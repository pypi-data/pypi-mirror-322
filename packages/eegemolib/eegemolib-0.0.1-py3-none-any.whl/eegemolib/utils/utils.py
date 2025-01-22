from pathlib import Path
import yaml
import os
import re
import torch
import random
import pickle
import numpy as np

def check_file(file):
    file_path = Path(file)

    if file_path.is_file():
        return True
    else:
        return False

def check_dir(file):
    file_path = Path(file)

    if file_path.is_dir():
        return True
    else:
        return False

def check_yaml(file: str):
    return Path(file).suffix in ('.yaml', '.yml')

def check_cache(path):
    if path.endswith(".cache"):  
        return path
    file_path = ''
    for filename in os.listdir(path): 
        if filename.endswith(".cache"):  
            file_path = os.path.join(path, filename) 
    return file_path

def load_cache(path):
    cache_path = check_cache(path)
    with open(cache_path, 'rb') as file:  
            cache_data = pickle.load(file)  
            # 假设cache_data是一个字典，包含了'train'数据  
            data = cache_data['data']
            label = cache_data['label']  
    print(f"load cache from {path}")
    return data, label


def load_yaml(file='default.yaml', parent_dir='./cfg'):
    """
    Load YAML data from a file. 

    If the path is absolute path, load directly
    elif the path is under cfg folder, try join './cfg' and yaml path together
    else path wrong

    Args:
        file (str, optional): File name. Default is 'data.yaml'.

    Returns:
        (dict): YAML data and file name.
    """
    assert Path(file).suffix in ('.yaml', '.yml'), f'Attempting to load non-YAML file {file} with yaml_load()'
    
    if (check_file(file)):
        pass
    else:
        if(check_file(os.path.join(parent_dir, file))):
            file = os.path.join(parent_dir, file)
        else:
            assert False, f"Attempting to load wrong path {str(file)} with yaml_load()"
    
    with open(file, errors='ignore', encoding='utf-8') as f:
        s = f.read()  # string

        # Remove special characters
        if not s.isprintable():
            s = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+', '', s)

        # Add YAML filename to dict and return
        data = yaml.safe_load(s) or {}  # always return a dict (yaml.safe_load() may return None for empty files)
      
        return data

def save_cache(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    
def yaml_save(file='data.yaml', data=None, header=''):
    """
    Save YAML data to a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        data (dict): Data to save in YAML format.
        header (str, optional): YAML header to add.

    Returns:
        (None): Data is saved to the specified file.
    """
    if data is None:
        data = {}
    file = Path(file)
    if not file.parent.exists():
        # Create parent directories if they don't exist
        file.parent.mkdir(parents=True, exist_ok=True)

    # Convert Path objects to strings
    valid_types = int, float, str, bool, list, tuple, dict, type(None)
    for k, v in data.items():
        if not isinstance(v, valid_types):
            data[k] = str(v)

    # Dump data to file in YAML format
    with open(file, 'w', errors='ignore', encoding='utf-8') as f:
        if header:
            f.write(header)
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def select_device(device_input):
    if device_input == -1:
        device = torch.device("cpu")
    elif isinstance(device_input, int):
        device = torch.device(f"cuda:{device_input}") 
    elif (isinstance(device_input, list) and all(isinstance(i, int) for i in device_input)): 
        device = [torch.device(f"cuda:{i}") for i in device_input] 
    else:
        raise ValueError("Invalid device input. Please provide -1 for CPU or a non-negative integer or list of non-negative integers for GPU.") 

    return device

def show_args(args, output='args'):
    print(f"=================== {output} settings ================")
    for key, value in args.items():
        print(f"{key}: {value}")
    
    print()
    

def init_seeds(seed=0, deterministic=False):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # for Multi-GPU, exception safe
    # torch.backends.cudnn.benchmark = True  # AutoBatch problem https://github.com/ultralytics/yolov5/issues/9287
    if deterministic:
        if TORCH_2_0:
            torch.use_deterministic_algorithms(True, warn_only=True)  # warn if deterministic is not possible
            torch.backends.cudnn.deterministic = True
            os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
            os.environ['PYTHONHASHSEED'] = str(seed)
        else:
            print('WARNING ⚠️ Upgrade to torch>=2.0.0 for deterministic training.')
    else:
        torch.use_deterministic_algorithms(False)
        torch.backends.cudnn.deterministic = False

def get_save_dir(name):
    run_path = os.path.join('./runs', name)
    weight_path = os.path.join(run_path, 'weights')

    if not os.path.exists(run_path):
        os.makedirs(run_path)
        os.makedirs(weight_path)

    return run_path, weight_path
    
def one_cycle(y1=0.0, y2=1.0, steps=100):
    """Returns a lambda function for sinusoidal ramp from y1 to y2 https://arxiv.org/pdf/1812.01187.pdf."""
    return lambda x: max((1 - math.cos(x * math.pi / steps)) / 2, 0) * (y2 - y1) + y1
