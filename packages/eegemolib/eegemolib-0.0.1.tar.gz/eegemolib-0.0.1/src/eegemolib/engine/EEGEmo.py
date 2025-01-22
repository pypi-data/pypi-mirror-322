from pathlib import Path
from typing import Union
from torch import nn
import time
from datetime import datetime, timedelta
import torch
import os
import math
from torch import nn, optim
from torch.nn import *

# own package
from utils.utils import load_yaml, select_device, show_args, get_save_dir, init_seeds, yaml_save, check_yaml
from data import create_dataset
from models import create_model
from preprocess import create_preprocess
from nn.tasks import load_pt, build_optimizer


class EEGEmo(nn.Module):
    """
    A base class for EEGEmoLib.
    Args:
        model(str, Path): Path to the model file to load or create
        overrides: overrides part parameters in given default.yaml
        task: classify / regression/ multi-label classify, default = classifiy
    Attributes:
        task: classify / regression/ multi-label classify
        ckpt: pretrained model path
    Methods:

    """
    def __init__(self, model: Union[str, Path] = 'default.yaml', **overrides):
        super().__init__()
        # TODO: set callbacks
        # self.callbacks = callbacks.get_default_callbacks()

        model = str(model).strip() # strip spaces
        self.overrides = overrides

        if Path(model).suffix in ['.yaml', '.yml']:
            self._new(model, self.overrides)
        elif Path(model).suffix in ['.pt', '.pth']:
            # TODO: 还没有完成模型加载的部分
            self._load(model)
        else:
            assert False, f"current model path {model} does not match .yaml .yml .pt"

    def train(self, **kwargs):
        """
        Train the model on a given datset
        """
        # update parameters 在train之前再更新一下参数设置
        overrides = load_yaml(kwargs['cfg']) if kwargs.get('cfg') and check_yaml(kwargs['cfg']) else self.args
        self.args = {**overrides, **kwargs} # update args
        self.data_args = load_yaml(kwargs['data'], parent_dir='./cfg/datasets') if kwargs.get('data') and check_yaml(kwargs['data']) else self.data_args
        self.model_args = load_yaml(kwargs['model'], parent_dir='./cfg/models/') if kwargs.get('model') and check_yaml(kwargs['model'])else self.model_args
        # print args for debug and check
        show_args(self.args)
        show_args(self.data_args, output='dataset')
        show_args(self.model_args, output='model')

        self._setup_train()

        nb = len(self.train_loader)
        self.epoch_time = None
        self.epoch_time_start = time.time()
        self.train_time_start = time.time()

        for epoch in range(self.start_epoch, self.args['epochs']):
            self.epoch = epoch
            self.model.train()
            pbar = enumerate(self.train_loader)
            for i, batch in pbar:
                # TODO: warm up, loss accumulate
                batch_data = batch['data'].to(torch.float32).to(self.device)
                batch_label = batch['label'].to(torch.float32).to(self.device)
                output = self.model(batch_data)
                # print(output, batch_label)
                self.loss = self.criterion(output, batch_label) # + 0.5 * self.l1(output, batch_label)
               
                self.loss.backward()
                self.optimizer.step()
                self.optimizer.zero_grad()
            
            if epoch % 5 == 0:
                print("loss:", self.loss)

            acc = 0 # 简单写个准确率计算的方法
            if epoch % 10 == 0: # test accuracy
                test_pbar = enumerate(self.test_loader)
                for i, batch in test_pbar:
                    batch_data = batch['data'].to(torch.float32).to(self.device)
                    batch_label = batch['label'].to(torch.float32).to(self.device)
                    output = self.model(batch_data)
                    if batch_label.argmax(dim = -1) == output.argmax(dim = -1):
                        acc = acc + 1.0
                    
                acc = acc / len(self.test_loader)
                print("accuracy:", acc, len(self.test_loader))


        # TODO: visual, log, save model, scheduler, early stopping, 

    def _setup_train(self):
        """
        Build device, model, dataloader and optimizers
        """
        # load data
        create_preprocess(self.data_args) # 根据./cfg/datasets/下的yaml设置预处理，特征提取，特征降维，训练测试集合划分
        self.train_loader = create_dataset({**self.data_args, **self.args})
        self.test_loader = create_dataset({**self.data_args, **self.args}, test=True)

        # model initialize
        self.start_epoch = 0
        self.epochs = self.args['epochs']
        # self.check_resume(self.args)
        self.device = select_device(self.args['device'])
        self.model = create_model(self.args['model'], self.args['model_type'])
        self.model = self.model.to(self.device) # fetch model to device cpu or gpu
        init_seeds(self.args['seed'])
        self.save_dir, self.weight_save_dir = get_save_dir(self.args['project_name'])
        yaml_save(os.path.join(self.save_dir, 'args.yaml'), self.args)

        # TODO: freeze layer, 还没做完，需要把freeze_list和model的搭建对应上才能freeze住，不然找不到对应的层
        freeze_list = self.args['freeze'] if isinstance(
            self.args['freeze'], list) else range(self.args.freeze) if isinstance(self.args.freeze, int) else []
        always_freeze_names = ['.dfl']  # always freeze these layers
        freeze_layer_names = [f'model.{x}.' for x in freeze_list] + always_freeze_names
        for k, v in self.model.named_parameters():
            if any(x in k for x in freeze_layer_names):
                LOGGER.info(f"Freezing layer '{k}'")
                v.requires_grad = False
            elif not v.requires_grad:
                LOGGER.info(f"WARNING ⚠️ setting 'requires_grad=True' for frozen layer '{k}'. "
                            'See ultralytics.engine.trainer for customization of frozen layers.')
                v.requires_grad = True
        
        # TODO: parallel training， 后面看有没有需要加吧，不一定要做并行化处理
        
        # Optimizer
        self.accumulate = max(round(self.args['nbs'] / self.args['batch_size']), 1)
        weight_decay = self.args['weight_decay'] * self.args['batch_size'] * self.accumulate / self.args['nbs'] # scale weight decay according to nbs setting
        iterations = math.ceil(len(self.train_loader)) / max(self.args['batch_size'], self.args['nbs']) * self.args['epochs']
        self.optimizer = self._build_optimizer(model=self.model,
                                        name=self.args['optimizer'],
                                        lr=self.args['lr0'],
                                        momentum=self.args['momentum'],
                                        decay=weight_decay,
                                        iterations=iterations)

        # Scheduler
        self._build_scheduler()
        # TODO: early stopping
        # self.stopper, self.stop = EarlyStopping(patience=self.args.patience), False
        # TODO: load pre-trained model

        self._build_loss()

    def _build_optimizer(self, model, name='auto', lr=0.001, momentum=0.9, decay=1e-5, iterations=1e5):
        """
        Constructs an optimizer for the given model, based on the specified optimizer name, learning rate, momentum,
        weight decay, and number of iterations.

        Args:
            model (torch.nn.Module): The model for which to build an optimizer.
            name (str, optional): The name of the optimizer to use. If 'auto', the optimizer is selected
                based on the number of iterations. Default: 'auto'.
            lr (float, optional): The learning rate for the optimizer. Default: 0.001.
            momentum (float, optional): The momentum factor for the optimizer. Default: 0.9.
            decay (float, optional): The weight decay for the optimizer. Default: 1e-5.
            iterations (float, optional): The number of iterations, which determines the optimizer if
                name is 'auto'. Default: 1e5.

        Returns:
            (torch.optim.Optimizer): The constructed optimizer.
        """
        g = [], [], []  # optimizer parameter groups
        bn = tuple(v for k, v in nn.__dict__.items() if 'Norm' in k)  # normalization layers, i.e. BatchNorm2d()
        if name == 'auto':
            LOGGER.info(f"{colorstr('optimizer:')} 'optimizer=auto' found, "
                        f"ignoring 'lr0={self.args.lr0}' and 'momentum={self.args.momentum}' and "
                        f"determining best 'optimizer', 'lr0' and 'momentum' automatically... ")
            nc = getattr(model, 'nc', 10)  # number of classes
            lr_fit = round(0.002 * 5 / (4 + nc), 6)  # lr0 fit equation to 6 decimal places
            name, lr, momentum = ('SGD', 0.01, 0.9) if iterations > 10000 else ('AdamW', lr_fit, 0.9)
            self.args.warmup_bias_lr = 0.0  # no higher than 0.01 for Adam

        for module_name, module in model.named_modules():
            for param_name, param in module.named_parameters(recurse=False):
                fullname = f'{module_name}.{param_name}' if module_name else param_name
                if 'bias' in fullname:  # bias (no decay)
                    g[2].append(param)
                elif isinstance(module, bn):  # weight (no decay)
                    g[1].append(param)
                else:  # weight (with decay)
                    g[0].append(param)

        if name in ('Adam', 'Adamax', 'AdamW', 'NAdam', 'RAdam'):
            optimizer = getattr(optim, name, optim.Adam)(g[2], lr=lr, betas=(momentum, 0.999), weight_decay=0.0)
        elif name == 'RMSProp':
            optimizer = optim.RMSprop(g[2], lr=lr, momentum=momentum)
        elif name == 'SGD':
            optimizer = optim.SGD(g[2], lr=lr, momentum=momentum, nesterov=True)
        else:
            raise NotImplementedError(
                f"Optimizer '{name}' not found in list of available optimizers "
                f'[Adam, AdamW, NAdam, RAdam, RMSProp, SGD, auto].'
                'To request support for addition optimizers please visit https://github.com/ultralytics/ultralytics.')

        optimizer.add_param_group({'params': g[0], 'weight_decay': decay})  # add g0 with weight_decay
        optimizer.add_param_group({'params': g[1], 'weight_decay': 0.0})  # add g1 (BatchNorm2d weights)
        print(
            f"optimizer: {type(optimizer).__name__}(lr={lr}, momentum={momentum}) with parameter groups "
            f'{len(g[1])} weight(decay=0.0), {len(g[0])} weight(decay={decay}), {len(g[2])} bias(decay=0.0)')
        return optimizer

    def _build_scheduler(self):
        """ Initialize training learning rate scheduler """
        if self.args['cos_lr']:
            self.lf = one_cycle(1, self.args['lrf'], self.epochs)  # cosine 1->hyp['lrf']
        else:
            self.lf = lambda x: max(1 - x / self.epochs, 0) * (1.0 - self.args['lrf']) + self.args['lrf']  # linear
            self.scheduler = optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda=self.lf)
    
    def _build_loss(self):
        self.criterion = nn.CrossEntropyLoss()
        self.l1 = nn.L1Loss()

    # TODO
    def test(self):
        pass
    
    def val(self):
        pass
    
    def export(self): # .pt -> .onnx
        pass
    
    def resume_training(self):
        pass

    def setup_model(self, model: str):
        pass
    
    def _new(self, cfg: str, overrides):
        """
        Initializes a model from .yaml or .yml
        
        Args:
            cfg(str): model configuration file
        """
        self.cfg = cfg
        self.args = load_yaml(cfg)
        self.args = {**self.args, **overrides}

        self.data_cfg = self.args['data']
        self.data_args = load_yaml(self.data_cfg, parent_dir='./cfg/datasets')

        self.model_cfg = self.args['model']
        self.model_type = self.args['model_type']
        self.model_args = load_yaml(self.model_cfg, parent_dir=f'./cfg/models/{self.model_type}')

        print(f"load global setting from {self.cfg}\nload dataset setting from {self.data_cfg}\nload model setting from {self.model_cfg}")

    def _load(self, weight: str):
        """
        Initializes a new model from .pt / .pth

        Args:
            weight: model checkpoint to be loaded
        """

        self.model = load_pt(weight)
        # TODO: update self.args according to self.model.args
        # self.args = {**self.args, self.model.args}
        


