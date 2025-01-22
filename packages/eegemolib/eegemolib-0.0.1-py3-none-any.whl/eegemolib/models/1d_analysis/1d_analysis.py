from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import GridSearchCV
import torch


class oneD_analysis:
    """
        data for training: torch.tensor, in shape [batch, channel, (band, )feature/time]
    """
    def __init__(self, classes_num, params, feature_dim=-1):
        super(oneD_analysis, self).__init__()
        self.numClasses = classes_num
        self.params = params
        self.featureDIM = feature_dim
        self.classifier = None
        self.regressor = None

    def classify(self, data, label):
        train_data, train_label = self.reformat(data, label)
        self.classifier.fit(train_data, train_label)

    def regress(self, data, label):
        train_data, train_label = self.reformat(data, label)
        self.regressor.fit(train_data, train_label)

    def fit(self, data, method="regress"):
        if method == "classify":
            output = self.classifier.predict(data)
        else:
            assert method == "regress"
            output = self.regressor.predict(data)
        return output

    def reformat(self, data, label):
        data = torch.tensor(data)
        b = data.size(0)
        # Section: reformat input into [batch, num_features]
        data = data.squeeze().reshape([-1, data.size(self.featureDIM)])
        multiplied = data.size(0) // b
        label = label.repeat_interleave(multiplied)
        return data, label


# TODO: grid search best parameters
class SVM(oneD_analysis):
    def __init__(self, classes_num, params: dict, feature_dim=-1):
        super(SVM, self).__init__(classes_num, params, feature_dim)
        assert classes_num == 2
        self.default_svr_params = {'kernel': params['kernel'] if params.__contains__('kernel') else 'rbf',
                                   'degree': params['degree'] if params.__contains__('degree') else 3,
                                   'gamma': params['gamma'] if params.__contains__('gamma') else 'scale',
                                   'coef0': params['coef0'] if params.__contains__('coef0') else 0.0,
                                   'tol': params['tol'] if params.__contains__('tol') else 0.001,
                                   'C': params['C'] if params.__contains__('C') else 1.0,
                                   'epsilon': params['epsilon'] if params.__contains__('epsilon') else 0.1,
                                   'shrinking': params['shrinking'] if params.__contains__('shrinking') else True,
                                   'cache_size': params['cache_size'] if params.__contains__('cache_size') else 200,
                                   'verbose': params['verbose'] if params.__contains__('verbose') else False,
                                   'max_iter': params['max_iter'] if params.__contains__('max_iter') else -1
                                   }
        self.default_svc_params = {'kernel': params['kernel'] if params.__contains__('kernel') else 'rbf',
                                   'degree': params['degree'] if params.__contains__('degree') else 3,
                                   'gamma': params['gamma'] if params.__contains__('gamma') else 'scale',
                                   'coef0': params['coef0'] if params.__contains__('coef0') else 0.0,
                                   'tol': params['tol'] if params.__contains__('tol') else 0.001,
                                   'C': params['C'] if params.__contains__('C') else 1.0,
                                   'probability': params['probability'] if params.__contains__('probability') else False,
                                   'shrinking': params['shrinking'] if params.__contains__('shrinking') else True,
                                   'cache_size': params['cache_size'] if params.__contains__('cache_size') else 200,
                                   'verbose': params['verbose'] if params.__contains__('verbose') else False,
                                   'max_iter': params['max_iter'] if params.__contains__('max_iter') else -1,
                                   'class_weight': params['class_weight'] if params.__contains__('class_weight') else None,
                                   'decision_function_shape': params['decision_function_shape'] if params.__contains__('decision_function_shape') else 'ovr',
                                   'break_ties': params['break_ties'] if params.__contains__('break_ties') else False,
                                   'random_state': params['random_state'] if params.__contains__('random_state') else None
                                   }
        self.classifier = SVC(**self.default_svc_params)
        self.regressor = SVR(**self.default_svr_params)
        # self.default_params = {'kernel': ['rbf'], 'C': [1, 10, 100, 1000], 'gamma': [1, 0.1, 0.01, 0.001],  'max_iter': [1e8]}


class RandomForest(oneD_analysis):
    def __init__(self, classes_num, params, feature_dim=-1):
        super(RandomForest, self).__init__(classes_num, params, feature_dim)
        self.default_regress_params = {
            'n_estimators': params['n_estimators'] if params.__contains__('n_estimators') else 100,
            'criterion': params['criterion'] if params.__contains__('criterion') else 'squared_error',
            'max_depth': params['max_depth'] if params.__contains__('max_depth') else None,
            'min_samples_split': params['min_samples_split'] if params.__contains__('min_samples_split') else 2,
            'min_samples_leaf': params['min_samples_leaf'] if params.__contains__('min_samples_leaf') else 1,
            'min_weight_fraction_leaf': params['min_weight_fraction_leaf'] if params.__contains__('min_weight_fraction_leaf') else 0.0,
            'max_features': params['max_features'] if params.__contains__('max_features') else 1.0,
            'max_leaf_nodes': params['max_leaf_nodes'] if params.__contains__('max_leaf_nodes') else None,
            'min_impurity_decrease': params['min_impurity_decrease'] if params.__contains__('min_impurity_decrease') else 0.0,
            'bootstrap': params['bootstrap'] if params.__contains__('bootstrap') else True,
            'oob_score': params['oob_score'] if params.__contains__('oob_score') else False,
            'n_jobs': params['n_jobs'] if params.__contains__('n_jobs') else None,
            'random_state': params['random_state'] if params.__contains__('random_state') else None,
            'verbose': params['verbose'] if params.__contains__('verbose') else 0,
            'warm_start': params['warm_start'] if params.__contains__('warm_start') else False,
            'ccp_alpha': params['ccp_alpha'] if params.__contains__('ccp_alpha') else 0.0,
            'max_samples': params['max_samples'] if params.__contains__('max_samples') else None
        }
        self.default_classifier_params = {
            'n_estimators': params['n_estimators'] if params.__contains__('n_estimators') else 100,
            'criterion': params['criterion'] if params.__contains__('criterion') else 'squared_error',
            'max_depth': params['max_depth'] if params.__contains__('max_depth') else None,
            'min_samples_split': params['min_samples_split'] if params.__contains__('min_samples_split') else 2,
            'min_samples_leaf': params['min_samples_leaf'] if params.__contains__('min_samples_leaf') else 1,
            'min_weight_fraction_leaf': params['min_weight_fraction_leaf'] if params.__contains__(
                'min_weight_fraction_leaf') else 0.0,
            'max_features': params['max_features'] if params.__contains__('max_features') else 1.0,
            'max_leaf_nodes': params['max_leaf_nodes'] if params.__contains__('max_leaf_nodes') else None,
            'min_impurity_decrease': params['min_impurity_decrease'] if params.__contains__(
                'min_impurity_decrease') else 0.0,
            'bootstrap': params['bootstrap'] if params.__contains__('bootstrap') else True,
            'oob_score': params['oob_score'] if params.__contains__('oob_score') else False,
            'n_jobs': params['n_jobs'] if params.__contains__('n_jobs') else None,
            'random_state': params['random_state'] if params.__contains__('random_state') else None,
            'verbose': params['verbose'] if params.__contains__('verbose') else 0,
            'warm_start': params['warm_start'] if params.__contains__('warm_start') else False,
            'ccp_alpha': params['ccp_alpha'] if params.__contains__('ccp_alpha') else 0.0,
            'max_samples': params['max_samples'] if params.__contains__('max_samples') else None,
            'class_weight': params['class_weight'] if params.__contains__('class_weight') else None
        }
        self.classifier = RandomForestClassifier(**self.default_classifier_params)
        self.regressor = RandomForestRegressor(**self.default_regress_params)
        # self.default_params = {'n_estimators': [5, 10, 20], 'max_features': [2, 4, 6, 8]}


class NearestNeighbors(oneD_analysis):
    def __init__(self, classes_num, params, feature_dim=-1):
        super(NearestNeighbors, self).__init__(classes_num, params, feature_dim)
        self.default_classifier_params = {
            'n_neighbors': params['n_neighbors'] if params.__contains__('n_neighbors') else 5,
            'weights': params['weights'] if params.__contains__('weights') else 'uniform',
            'algorithm': params['algorithm'] if params.__contains__('algorithm') else 'auto',
            'leaf_size': params['leaf_size'] if params.__contains__('leaf_size') else 30,
            'p': params['p'] if params.__contains__('p') else 2,
            'metric': params['metric'] if params.__contains__('metric') else 'minkowski',
            'metric_params': params['metric_params'] if params.__contains__('metric_params') else None,
            'n_jobs': params['n_jobs'] if params.__contains__('n_jobs') else None
        }
        self.default_regression_params = {
            'n_neighbors': params['n_neighbors'] if params.__contains__('n_neighbors') else 5,
            'weights': params['weights'] if params.__contains__('weights') else 'uniform',
            'algorithm': params['algorithm'] if params.__contains__('algorithm') else 'auto',
            'leaf_size': params['leaf_size'] if params.__contains__('leaf_size') else 30,
            'p': params['p'] if params.__contains__('p') else 2,
            'metric': params['metric'] if params.__contains__('metric') else 'minkowski',
            'metric_params': params['metric_params'] if params.__contains__('metric_params') else None,
            'n_jobs': params['n_jobs'] if params.__contains__('n_jobs') else None
        }
        self.classifier = KNeighborsClassifier(**self.default_classifier_params)
        self.regressor = KNeighborsRegressor(**self.default_regression_params)
        # self.default_params = {'kernel': ['rbf'], 'C': [1, 10, 100, 1000], 'gamma': [1, 0.1, 0.01, 0.001],  'max_iter': [1e8]}


class LinearRegression(oneD_analysis):
    def __init__(self, classes_num, params, feature_dim=-1):
        super(LinearRegression, self).__init__(classes_num, params, feature_dim)
        self.default_params = {
            'fit_intercept': params['fit_intercept'] if params.__contains__('fit_intercept') else True,
            'normalize': params['normalize'] if params.__contains__('normalize') else False,
            'copy_X': params['copy_X'] if params.__contains__('copy_X') else True,
            'n_jobs': params['n_jobs'] if params.__contains__('n_jobs') else None,
            'positive': params['positive'] if params.__contains__('positive') else False
        }

    def classify(self, data, label):
        raise NotImplementedError


class HiddenMarkovModel(oneD_analysis):
    def __init__(self, classes_num, params, feature_dim=-1):
        super(HiddenMarkovModel, self).__init__(classes_num, params, feature_dim)
        self.default_params = {
            'n_components': params['n_components'] if params.__contains__('n_components') else 1,
            'startprob_prior': params['startprob_prior'] if params.__contains__('startprob_prior') else 1.0,
            'transmat_prior': params['transmat_prior'] if params.__contains__('transmat_prior') else 1.0,
            'covariance_type': params['covariance_type'] if params.__contains__('covariance_type') else 'diag',
            'min_covar': params['min_covar'] if params.__contains__('min_covar') else 0.001,
            'means_prior': params['means_prior'] if params.__contains__('means_prior') else 0,
            'means_weight': params['means_weight'] if params.__contains__('means_weight') else 0,
            'covars_prior': params['covars_prior'] if params.__contains__('covars_prior') else 0.01,
            'covars_weight': params['covars_weight'] if params.__contains__('covars_weight') else 1,
            'algorithm': params['algorithm'] if params.__contains__('algorithm') else 'viterbi',
            'random_state': params['random_state'] if params.__contains__('random_state') else None,
            'n_iter': params['n_iter'] if params.__contains__('n_iter') else 10,
            'tol': params['tol'] if params.__contains__('tol') else 0.01,
            'verbose': params['verbose'] if params.__contains__('verbose') else False,
            'params': params['params'] if params.__contains__('params') else 'stmc',
            'init_params': params['init_params'] if params.__contains__('init_params') else 'stmc',
            'implementation': params['implementation'] if params.__contains__('implementation') else 'log'
        }
        self.regressor = GaussianHMM(**self.default_params)

    def classify(self, data, label):
        raise NotImplementedError

    def regress(self, data, label):
        """
        :param data: (array-like, shape (n_samples, n_features)) – Feature matrix of individual samples.
        :param label: (array-like of integers, shape (n_sequences, )) – Lengths of the individual sequences in X. The sum of these should be n_samples.
        """
        train_data, train_label = self.reformat(data, label)
        self.regressor.fit(train_data)

    # Section: fit
    #    """
    #    :return: state_sequence (array, shape (n_samples, )) – Labels for each sample from X.
    #    """
