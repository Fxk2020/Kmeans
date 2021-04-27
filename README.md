# 聚类算法

## 一、原型聚类1--Kmeans聚类！！！

K Means Clustering with Python

### 版本一--数据只有两维，上传格式为txt文件

### 版本二--数据只有两维，但是上传文件的格式增加了xlsx和xls文件

### 版本三--数据有多维，可以上传的格式可以是xlsx和xls

1. 选择初始化的 k 个样本作为初始聚类中心 ![[公式]](https://www.zhihu.com/equation?tex=a%3D%7Ba_1%2Ca_2%2C%E2%80%A6a_k%7D) ；
2. 针对数据集中每个样本 ![[公式]](https://www.zhihu.com/equation?tex=x_i) 计算它到 k 个聚类中心的距离并将其分到距离最小的聚类中心所对应的类中；
3. 针对每个类别 ![[公式]](https://www.zhihu.com/equation?tex=a_j) ，重新计算它的聚类中心 ![[公式]](https://www.zhihu.com/equation?tex=a_j%3D%5Cfrac%7B1%7D%7B%5Cleft%7C+c_i+%5Cright%7C%7D%5Csum_%7Bx%5Cin+c_i%7Dx) （即属于该类的所有样本的质心）；
4. 重复上面 2 3 两步操作，直到达到某个中止条件（迭代次数、最小误差变化等）。



python实现：

```python
# 创建模型，进行聚类
kmeans = KMeans(n_clusters=k)
kmeans.fit(values)

# 获取中心点和标签
centers = kmeans.cluster_centers_
labels = kmeans.labels_
```

fit：对数据进行聚类

cluster_centers_：聚类中心点

kmeans.labels_：聚类的标签



![](/img/kmeans.png)

### 2.学习向量机聚类--数据必须有标签

学习向量量化(Learning Vector Quantization)，简称LVQ；

**思路**：

-  初始化几个向量作为原型向量；
-  样本集中随机选取样本，计算和原型向量的距离，找出最邻近的原型向量；
-  比较**标签**是否一样，一样的话原型向量向样本按照学习率靠拢，否则远离；
-  不断的迭代，直到满足迭代的停止条件(最大迭代轮次、原型向量的更新阈值等)。

![](/img/lvq.png)



**没有python实现代码，不常用**



### 3.高斯混合聚类方法

GMM(Gaussian mixtures)

**优点:**GMM的优点是投影后样本点不是得到一个确定的分类标记，而是得到每个类的概率，这是一个重要信息。GMM不仅可以用在聚类上，也可以用在概率密度估计上。**缺点:**当每个混合模型没有足够多的点时，估算协方差变得困难起来，同时算法会发散并且找具有无穷大似然函数值的解，除非人为地对协方差进行正则化。GMM每一步迭代的计算量比较大，大于k-means。GMM的求解办法基于EM算法，因此有可能陷入局部极值，这和初始值的选取十分相关了。

#### python实现

`sklearn.mixture` 是一个应用高斯混合模型进行非监督学习的包(支持 diagonal，spherical，tied，full 四种协方差矩阵), *（注：diagonal 指每个分量有各自独立的对角协方差矩阵， spherical 指每个分量有各自独立的方差(再注:spherical是一种特殊的 diagonal, 对角的元素相等)， tied 指所有分量共享一个标准协方差矩阵， full 指每个分量有各自独立的标准协方差矩阵）*，它可以对数据进行抽样，并且根据数据来估计模型。同时该包也支持由用户来决定模型内混合的分量数量。 *（译注：在高斯混合模型中，我们将每一个高斯分布称为一个分量，即 component）*

```python
estimators = GaussianMixture(n_components=n_classes,
                             covariance_type=covariance_type, max_iter=20, random_state=0)

estimators.fit(X_train)
y_predict = estimators.predict(X_train)
```

n_components:是聚类的个数；

fit是进行高斯混合聚类；

predict是获得数据聚类的标签。



![](/img/gmm.png)

## 二、概率聚类

dbscan方法

1、以每一个数据点 xi 为圆心，以 eps 为半径画一个圆圈。这个圆圈被称为 xi 的 eps 邻域

2、对这个圆圈内包含的点进行计数。如果一个圆圈里面的点的数目超过了密度阈值 MinPts，那么将该圆圈的圆心记为核心点，又称核心对象。如果某个点的 eps 邻域内点的个数小于密度阈值但是落在核心点的邻域内，则称该点为边界点。既不是核心点也不是边界点的点，就是噪声点。

3、核心点 xi 的 eps 邻域内的所有的点，都是 xi 的直接密度直达。如果 xj 由 xi 密度直达，xk 由 xj 密度直达。。。xn 由 xk 密度直达，那么，xn 由 xi 密度可达。这个性质说明了由密度直达的传递性，可以推导出密度可达。

4、如果对于 xk，使 xi 和 xj 都可以由 xk 密度可达，那么，就称 xi 和 xj 密度相连。将密度相连的点连接在一起，就形成了我们的聚类簇。

DBSCAN 的核心概念是 *core samples*, 是指位于高密度区域的样本。 因此一个簇是一组核心样本，每个核心样本彼此靠近（通过某个距离度量测量） 和一组接近核心样本的非核心样本（但本身不是核心样本）。算法中的两个参数, `min_samples` 和 `eps`,正式的定义了我们所说的 *稠密（dense）*。较高的 `min_samples` 或者较低的 `eps` 都表示形成簇所需的较高密度。

#### python实现

```python
y_pred = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(data)
# 获取标签
labels = y_pred
```

eps：一个样本的两个样本之间的最大距离应视为另一个样本的邻域。

min_samples：将某个点视为核心点的邻域中的样本数量（或总权重）。

labels：预测的标签

![](/img/dbscan.png)

## 三、层次聚类

agglomerative方法

层次聚类(Hierarchical clustering)代表着一类的聚类算法，这种类别的算法通过不断的合并或者分割内置聚类来构建最终聚类。 聚类的层次可以被表示成树（或者树形图(dendrogram)）。树根是拥有所有样本的唯一聚类，叶子是仅有一个样本的聚类。

#### python实现

```python
ward = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
labels = ward.fit_predict(data)
```

n_clusters:聚类个数

affinity:用于计算链接的度量。 可以是“欧几里得”，“ l1”，“ l2”， “曼哈顿”，“余弦”或“预先计算”

linkage:使用哪个链接标准。 链接标准确定哪个观测值之间使用的距离。 该算法将合并最小化此标准的集群对

labels:预测的类别



![](/img/agglomerativeClustering.png)