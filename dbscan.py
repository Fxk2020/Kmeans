import time

import pylab
from sklearn.cluster import DBSCAN  # 用于概率聚类
from sklearn import datasets

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import xlrd
import xlwt
from pylab import mpl

import sys


def loadData(url):
    """
    :param url:待分析文件的路径
    :return: value_name实例变量名 x,y数据点的横纵坐标
    """
    # 指定默认字体
    # 在mac系统下中文显示
    mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    data = xlrd.open_workbook(url)
    table = data.sheet_by_name('data')

    x = []
    y = []
    value_name = []
    for row in range(1, table.nrows):
        value_name.append(table.cell_value(row,0))
        x.append(table.cell_value(row,1))
        y.append(table.cell_value(row,2))

    return value_name,x, y


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
    workbook.save(path + "/resultDbscan.xls")
    print("xls格式表格写入数据成功！")


def dbscan(inputUrl,outputDir,eps,min_samples):
    """
    dbscan方法聚类
    :param inputUrl: 源文件路径
    :param outputDir: 分析文件的输出路径
    :param eps:eps
    :param min_samples: min_samples
    :return: value_name变量名 labels数据标签
    """
    value_name,x, y = loadData(inputUrl)
    data = []
    for i in range(len(x)):
        value = [x[i], y[i]]
        data.append(value)

    y_pred = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(data)
    # 获取标签
    labels = y_pred

    # 转存图像
    plt.scatter(x, y, c=y_pred)
    tick = time.time()
    print("当前的时间戳为：", tick)
    pylab.savefig(outputDir + '/result.png')

    return value_name,labels


# 脚本入口
def main(inputUrl,outputDir,eps,min_samples):
    value_name,labels = dbscan(inputUrl,outputDir,eps,min_samples)
    write_excel_xls(outputDir,"result",value_name,labels)


if __name__ == '__main__':
    """
     DBSCAN算法参数，即我们的𝜖-邻域的距离阈值，和样本距离超过𝜖的样本点不在𝜖-邻域内。
     默认值是0.5.一般需要通过在多组值里面选择一个合适的阈值。
     eps过大，则更多的点会落在核心对象的𝜖-邻域，此时我们的类别数可能会减少，
     本来不应该是一类的样本也会被划为一类。反之则类别数可能会增大，本来是一类的样本却被划分开。

     DBSCAN算法参数，即样本点要成为核心对象所需要的𝜖-邻域的样本数阈值。
     默认值是5. 一般需要通过在多组值里面选择一个合适的阈值。
     通常和eps一起调参。在eps一定的情况下，min_samples过大，则核心对象会过少，
     此时簇内部分本来是一类的样本可能会被标为噪音点，类别数也会变多。
     反之min_samples过小的话，则会产生大量的核心对象，可能会导致类别数过少。

    """
    a = []
    # 其中sys.argv用于获取参数url1，url2等。而sys.argv[0]代表python程序名，所以列表从1开始读取参数。
    for i in range(1, len(sys.argv)):  # 一定要引入sys包！！！！！！
        a.append((sys.argv[i]))
    print(main(a[0], a[1], float(a[2]),int(a[3])))

# main("/Users/yuanbao/Desktop/kmeans算法/各地城市经纬度.xlsx","/Users/yuanbao/Desktop",0.3,5)
