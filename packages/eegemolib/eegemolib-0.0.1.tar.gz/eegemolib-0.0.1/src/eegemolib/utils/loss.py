import torch
import torch.nn.functional as F
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
from scipy.spatial import distance
from scipy.stats import entropy


class Loss:
    @staticmethod
    def CrossEntropy(output, target):
        return F.cross_entropy(output, target)

    @staticmethod
    def KullbackLeiblerDivergence(output, target):
        return F.kl_div(output, target)


class Metrics:
    @staticmethod
    def Accuracy(y_pred, y_true):
        _, predicted = torch.max(y_pred.data, 1)
        return accuracy_score(y_true, predicted)

    @staticmethod
    def F1(y_pred, y_true):
        _, predicted = torch.max(y_pred.data, 1)
        return f1_score(y_true, predicted, average='weighted')

    @staticmethod
    def Chebyshev(u, v):
        return distance.chebyshev(u, v)

    @staticmethod
    def clark_distance(u, v):
        n = len(u)
        mean_u_v = np.mean([u, v])
        sum_squared_difference = np.sum((u - v) ** 2)
        return np.sqrt(sum_squared_difference / (2 * (1 - mean_u_v)) * 1 / n)

    @staticmethod
    def Intersection(u, v):
        return sum(np.minimum(u, v))

    @staticmethod
    def Canberra(u, v):
        return distance.canberra(u, v)

    @staticmethod
    def Cosine(u, v):
        return distance.cosine(u, v)

    @staticmethod
    def KullbackLeibler(u, v):
        return entropy(u, v)