import time

import pylab
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import AgglomerativeClustering
from sklearn import decomposition
import sklearn

import xlrd
import xlwt
from pylab import mpl

import sys


def loadData(url):
    """
    :param url:待分析文件的路径
    :return: values, variables变量值和变量名
    """
    # 指定默认字体
    # 在mac系统下中文显示
    mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    data = xlrd.open_workbook(url)
    table = data.sheet_by_name('data')

    variables = []
    values = np.zeros((table.nrows - 1, table.ncols - 1))
    for row in range(1, table.nrows):
        row_value = []
        variables.append(table.cell_value(row, 0))
        for col in range(1, table.ncols):
            values[row - 1, col - 1] = table.cell_value(row, col)

    variables = np.array(variables)
    return values, variables


def write_excel_xls(path, sheet_name, variablesNames, labels):
    """
    用于将分析结果写入文件
    :param path: 输出路径
    :param sheet_name: 创建的表名
    :param variablesNames: 变量名
    :param labels: 标签
    :return: 成功创建表格
    """
    index = len(variablesNames)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格

    # 向表格中写入数据（对应的行和列）
    sheet.write(0, 0, "实例名称")
    for i in range(0, index):
        sheet.write(i + 1, 0, variablesNames[i])
    sheet.write(0, 1, "对应类别")
    for i in range(0, index):
        sheet.write(i + 1, 1, str(labels[i]))
    # 保存工作簿
    workbook.save(path + "/resultAgglomerative.xls")
    print("xls格式表格写入数据成功！")


def PCA(X, label, variablesName, outputDir):
    """
    根据两个最大的主成分进行绘图 降维为2，方便画图,输出图像并保存
    :param X: 聚类的源数据
    :param label: 聚完类之后的标签
    :param variablesName:变量名
    :return:直观的聚类结果图像
    """
    pca = decomposition.PCA(n_components=2)
    pca.fit(X)  # 主城分析时每一行是一个输入数据
    result = pca.transform(X)  # 计算结果
    plt.figure(figsize=[10, 6])  # 新建一张图进行绘制
    n_clusters = len(set(label.tolist()))
    for i in range(result[:, 0].size):
        color = cm.nipy_spectral(float(label[i]) / n_clusters)
        plt.plot(result[i, 0], result[i, 1],
                 c=color, marker='o', markersize=10)
        plt.text(result[i, 0], result[i, 1], variablesName[i])
    x_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[0] * 100.0), 2)  # x轴标签字符串
    y_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[1] * 100.0), 2)  # y轴标签字符串
    plt.xlabel(x_label)  # 绘制x轴标签
    plt.ylabel(y_label)  # 绘制y轴标签
    plt.title('使用主成分分析法对高维数据进行降维，产生直观图像')
    # 显示并保存散点图
    tick = time.time()
    print("当前的时间戳为：", tick)
    pylab.savefig(outputDir + '/result.png')


def agglomerative(inputUrl,outputDir,k):
    """
    进行层次聚类
    :param inputUrl
    :param outputDir
    :param k:聚类的个数
    :param data:聚类的数据
    :return:
    """
    data, variablesNames = loadData(inputUrl)
    ward = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
    labels = ward.fit_predict(data)

    # 画图
    PCA(X=data, label=labels, variablesName=variablesNames, outputDir=outputDir)

    # 保存文件
    write_excel_xls(outputDir,"result",variablesNames,labels)


# 脚本入口
def main(inputUrl,outputDir,k):
    agglomerative(inputUrl,outputDir,k)


if __name__ == '__main__':
    a = []
    # 其中sys.argv用于获取参数url1，url2等。而sys.argv[0]代表python程序名，所以列表从1开始读取参数。
    for i in range(1, len(sys.argv)):  # 一定要引入sys包！！！！！！
        a.append((sys.argv[i]))
    print(main(a[0], a[1], int(a[2])))

#
# main("/Users/yuanbao/Desktop/kmeans算法/data/data.xlsx","/Users/yuanbao/Desktop",3)
