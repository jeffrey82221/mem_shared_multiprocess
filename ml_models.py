from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_roc_curve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dataset = pd.read_csv('Book_Purchased.csv')
dataset['Purchased'] = dataset['Purchased'].astype('str')
dx = dataset.iloc[:, [2, 3, 4]].values
dy = dataset.iloc[:, 5].values
dx = PCA(n_components=2).fit_transform(dx)
dx = StandardScaler().fit_transform(dx)
dx_train, dx_test, dy_train, dy_test = train_test_split(dx, dy, test_size=0.2, random_state=0)

# 建立不同模型
models = [
    KNeighborsClassifier(),
    LogisticRegression(),
    LinearSVC(),
    SVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    XGBClassifier(),
    LGBMClassifier(),
    ]
# 訓練不同模型
for i, _ in enumerate(models):
    models[i].fit(dx_train, dy_train)
plt.rcParams['font.size'] = 12
plt.figure(figsize=(8, 8))
# 建立子圖表
ax = plt.subplot(111)
ax.set_title('ROC')
# 畫對角線
ax.plot([0, 1], [0, 1], color='grey',
        linewidth=2, linestyle='--')
# 對每個模型畫 ROC 曲線
for model in models:
    plot_roc_curve(model, dx_test, dy_test,
                   linewidth=5, alpha=0.5, ax=ax)
plt.grid(True)
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.tight_layout()
plt.show()