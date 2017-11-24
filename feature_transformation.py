from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
import pandas as pd

def pca(data):
    clf = PCA(n_components=1)
    X_train=clf.fit_transform(data)
    return pd.DataFrame(X_train).add_prefix("pca")

def kbest(left, right, k=15):
    kb = SelectKBest(score_func=f_regression, k=k)
    kb.fit(left, right)
    return left.columns[kb.get_support()]