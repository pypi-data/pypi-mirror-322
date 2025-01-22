import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA


def featureSelectionRFE(originalFeatures,originalLabels, num_remained,max_iter=500):
    """
        - originalFeatures<np.array>: (各时间窗为独立的样本点) [sample, features]
        # 若输入为时间序列，则先拆解[sample, feature, time] -> [sample*time, feature]
        - num_remained<int>: 保留的特征数目
    """
    assert len(originalFeatures)==len(originalLabels)
    # create the RFE model and select 3 attributes
    rfe = RFE(estimator=LogisticRegression(solver='lbfgs', max_iter=max_iter), n_features_to_select=num_remained)
    rfe = rfe.fit(originalFeatures,originalLabels)
    # summarize the selection of the attributes
    # print(rfe.support_)
    # print(rfe.ranking_)
    return originalFeatures[:,rfe.support_]


def featureSelectionPCA(originalFeatures,n_components=30):
    model = PCA(n_components=n_components)
    lower_dimensional_data = model.fit_transform(originalFeatures)
    print(f"降维后的特征维度数：{model.n_components_}")
    return lower_dimensional_data


if __name__ =='__main__':
    x=np.random.random((300,100))
    y=np.random.randint(0,5,size=[300,])
    rfe_feat=featureSelectionRFE(x,y,50)
    pca_feat=featureSelectionPCA(x)
    print(rfe_feat.shape,pca_feat.shape)

