# 从Excel中读取数据
# 导入模块
import time

import pylab
import xlrd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import openpyxl
import sys


def read_data_excel(url):
    data_points = []
    x_axis = []
    y_axis = []

    # 打开文件方式1：
    work_book = xlrd.open_workbook(url)
    # 获取工作簿中sheet表数量
    print(work_book.nsheets)
    # 获取工作簿中所有sheet表对象
    sheets = work_book.sheets()
    sheet_1 = work_book.sheet_by_index(0)

    #  获得行数和列数
    row_sum = sheet_1.nrows
    col_sum = sheet_1.ncols
    value = []
    for i in range(row_sum):
        value = (sheet_1.cell_value(i, 0),sheet_1.cell_value(i,1))
        x_axis.append(sheet_1.cell_value(i, 0))
        y_axis.append(sheet_1.cell_value(i,1))
        data_points.append(value)

    print(x_axis)
    return data_points,x_axis,y_axis


def main(k,url,outputUrl="/Users/yuanbao/Desktop/测试/文件上传"):

    data,x_axis,y_axis = read_data_excel(url)

    # 这里已经知道了分3类，其他分类这里的参数需要调试
    model = KMeans(n_clusters=k)

    # 训练模型
    model.fit(data)

    # 预测全部150条数据
    all_predictions = model.predict(data)

    # 打印出来对150条数据的聚类散点图
    plt.scatter(x_axis, y_axis, c=all_predictions)
    # 设置标题
    plt.title('K-means Scatter Diagram')
    # 设置X轴标签
    plt.xlabel('X')
    # 设置Y轴标签
    plt.ylabel('Y')

    # 详细输出原结果
    r_new = pd.concat([pd.DataFrame(data), pd.Series(model.labels_)], axis=1)
    names = ["x","y"]
    r_new.columns = names + [u'类别数目']

    # 显示并保存散点图
    tick = time.time()
    print("当前的时间戳为：", tick)
    pylab.savefig(outputUrl + '/result.png')
    r_new.to_excel(outputUrl + "/" + str(tick) + '.xlsx')  # 自定义一个路径，保存在excel里面
    # plt.show()


# 运行脚本
if __name__ == '__main__':

    a = []
    # 其中sys.argv用于获取参数url1，url2等。而sys.argv[0]代表python程序名，所以列表从1开始读取参数。
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    print(main(int(a[0]), a[1], a[2]))

# 测试包的版本
# print(xlrd.__version__)
# print(pd.__version__)
# print(openpyxl.__version__)

# 固定目录测试
# main(2,"/Users/yuanbao/Desktop/kmeans算法/dataDbscan.xlsx", "/Users/yuanbao/Desktop")


