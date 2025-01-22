from sklearn.feature_selection import *
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.decomposition import PCA
import numpy as np
from sklearn.svm import *
from sklearn.impute import SimpleImputer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


# TODO: 要加抽象类吗？还是每个方法单独实现就行？
############################ Filter  ####################
# Method 1: 方差选择法
def feature_Variance(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    VarianceThreshold(threshold=3).fit_transform(train_feature)

# Method2: PCA主成分分析
def feature_PCA(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    PCA(n_components=2).fit_transform(train_feature)

# Method3: LDA线性判别分析
def feature_LDA(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    # 处理缺失值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    train_feature = imp.fit_transform(train_feature)
    test_feature = imp.fit_transform(test_feature)

    lda = LinearDiscriminantAnalysis()
    lda.fit(train_feature, train_label)

    selected_train_feature = lda.transform(train_feature)
    selected_test_feature = lda.transform(test_feature)
    return selected_train_feature, train_label, selected_test_feature, test_label

############################ Wrapper  ####################
# Method 1: 递归式特征消除 （Recursive Feature Elimination）
def feature_RFE(train_feature, train_label, test_feature=None, test_label=None, num_features=10): # 这里的选择个数默认是10个了，可以调整,也可以在yaml里面控制
    # refer to: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html?highlight=rfe#sklearn.feature_selection.RFE
    # 处理缺失值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    train_feature = imp.fit_transform(train_feature)
    test_feature = imp.fit_transform(test_feature)

    estimator = SVR(kernel="linear")
    model = RFE(estimator, n_features_to_select=num_features, step=1) 
    fit = model.fit(train_feature, train_label)
    # 获取选定的特征索引
    selected_features_index = selector.support_

    # 根据选定的特征索引获取选定的特征
    selected_train_feature = train_feature[:, selected_features_index]
    selected_test_feature = test_feature[:, selected_features_index]

    return selected_train_feature, train_label, selected_test_feature, test_label

############################ Embedding  ####################
# Method 1: 逻辑回归
def feature_LR(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    pass

def feature_L1(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(train_feature, train_label)
    model = SelectFromModel(lsvc, prefit=True)
    X_new = model.transform(X)

# Method 2: 树模型
def feature_GBDT(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    SelectFromModel(GradientBoostingClassifier()).fit_transform(train_feature, train_label)

def feature_RandomForest(train_feature, train_label, test_feature, test_label, num_features=10):
    model = RandomForestRegressor(n_estimators=10, random_state=123)
    fit = model.fit(feature, label)

# Method 3: LASSO
def feature_LASSO(train_feature, train_label, test_feature=None, test_label=None, num_features=10):
    pass

