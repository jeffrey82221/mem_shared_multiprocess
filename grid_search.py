from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
import sharedmem
def to_shared(array):
    fp = sharedmem.empty(array.shape, dtype=array.dtype)
    fp[:] = array[:]
    return fp
# 載入鳶尾花朵資料集
iris = datasets.load_iris()
# 設定想要的搜索參數並給予候選值
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
# 建立 SVC 分類器
svc = svm.SVC()
# 網格搜索所有可能的組合(2*2)共四種
clf = GridSearchCV(svc, parameters)
# 擬合數據並回傳最佳模型
clf.fit(to_shared(iris.data), to_shared(iris.target))
# clf.fit(iris.data, iris.target)
print(clf.cv_results_)