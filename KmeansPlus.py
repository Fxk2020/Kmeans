import random
import time
from math import *
import matplotlib.pyplot as plt
import sys

# 从文件种读取数据
import pylab


def read_data(url):
    data_points = []
    with open(url, 'r') as fp:
        for line in fp:
            if line == '\n':
                continue
            data_points.append(tuple(map(float, line.split(' '))))  # 去掉空格，并将data中数据的类型转为tuple
        fp.close()
        return data_points


# 初始化聚类中心
def begin_cluster_center(data_points, k):
    center = []
    length = len(data_points)  # 长度
    rand_data = random.sample(range(0, length), k)  # 生成k个不同随机数
    for i in range(k):  # 得出k个聚类中心(随机选出)
        center.append(data_points[rand_data[i]])
    return center


# 计算最短距离（欧式距离）
def distance(a, b):
    length = len(a)
    sum = 0
    for i in range(length):
        sq = (a[i] - b[i]) ** 2
        sum += sq
    return sqrt(sum)


# 分配样本
# 按照最短距离将所有样本分配到k个聚类中心中的某一个
def assign_points(data_points, center, k):
    assignment = []
    for i in range(k):
        assignment.append([])
    for point in data_points:
        min = 10000000
        flag = -1
        for i in range(k):
            value = distance(point, center[i])  # 计算每个点到聚类中心的距离
            if value < min:
                min = value  # 记录距离的最小值
                flag = i  # 记录此时聚类中心的下标
        assignment[flag].append(point)
    return assignment


# 更新聚类中心,计算每一簇中所有点的平均值
def update_cluster_center(center, assignment, k):
    for i in range(k):  # assignment中的每一簇
        x = 0
        y = 0
        length = len(assignment[i])  # 每一簇的长度
        if length != 0:
            for j in range(length):  # 每一簇中的每个点
                x += assignment[i][j][0]  # 横坐标之和
                y += assignment[i][j][1]  # 纵坐标之和
            center[i] = (x / length, y / length)
    return center


# 计算平方误差
def getE(assignment, center):
    sum_E = 0
    for i in range(len(assignment)):
        for j in range(len(assignment[i])):
            sum_E += distance(assignment[i][j], center[i])
    return sum_E


# 计算各个聚类中心的新向量，更新距离，即每一类中每一维均值向量。
# 然后再进行分配，比较前后两个聚类中心向量是否相等，若不相等则进行循环，
# 否则终止循环，进入下一步。
def k_means(data_points, k):
    # 由于初始聚类中心是随机选择的，十分影响聚类的结果，聚类可能会出现有较大误差的现象
    # 因此如果由初始聚类中心第一次分配后有结果为空，重新选择初始聚类中心，重新再聚一遍，直到符合要求
    while 1:
        # 产生初始聚类中心
        begin_center = begin_cluster_center(data_points, k)
        # 第一次分配样本
        assignment = assign_points(data_points, begin_center, k)
        for i in range(k):
            if len(assignment[i]) == 0:  # 第一次分配之后有结果为空，说明聚类中心没选好，重新产生初始聚类中心
                continue
        break
    # 第一次的平方误差
    begin_sum_E = getE(assignment, begin_center)
    # 更新聚类中心
    end_center = update_cluster_center(begin_center, assignment, k)
    # 第二次分配样本
    assignment = assign_points(data_points, end_center, k)
    # 第二次的平方误差
    end_sum_E = getE(assignment, end_center)
    count = 2  # 计数器
    # 比较前后两个聚类中心向量是否相等
    # print(compare(end_center,begin_center)==False)
    while (begin_sum_E != end_sum_E):
        begin_center = end_center
        begin_sum_E = end_sum_E
        # 再次更新聚类中心
        end_center = update_cluster_center(begin_center, assignment, k)
        # 进行分配
        assignment = assign_points(data_points, end_center, k)
        # 计算误差
        end_sum_E = getE(assignment, end_center)
        count = count + 1  # 计数器加1
    return assignment, end_sum_E, end_center, count


# 打印并返回最终结果
def print_result(count, end_sum_E, k, assignment):
    # 打印最终聚类结果
    result = ""
    result += '经过' + str(count) + '次聚类，平方误差为：' + str(end_sum_E)
    result += '\n---------------------------------分类结果---------------------------------------'
    for i in range(k):
        result += '\n第' + str(i + 1) + '类数据：' + str(assignment[i])
    result += '\n--------------------------------------------------------------------------------\n'
    # print("result:", result)
    return result


def plot(k, assignment, center, result, outputUrl):
    # 初始坐标列表
    x = []
    y = []
    for i in range(k):
        x.append([])
        y.append([])
    # 填充坐标 并绘制散点图
    for j in range(k):
        for i in range(len(assignment[j])):
            x[j].append(assignment[j][i][0])  # 横坐标填充
        for i in range(len(assignment[j])):
            y[j].append(assignment[j][i][1])  # 纵坐标填充
        plt.scatter(x[j], y[j], marker='o')
        plt.scatter(center[j][0], center[j][1], c='b', marker='*')  # 画聚类中心
    # 设置标题
    plt.title('K-means Scatter Diagram')
    # 设置X轴标签
    plt.xlabel('X')
    # 设置Y轴标签
    plt.ylabel('Y')
    # 显示并保存散点图
    tick = time.time()
    print("当前的时间戳为：", tick)
    pylab.savefig(outputUrl + "/" + str(tick) + '.png')
    f = open(outputUrl + "/" + str(tick) + '.txt', "x")
    f.write(result)
    f.close()
    # plt.show()


def main(k=3, url="/Users/yuanbao/Desktop/kmeans算法/data.txt", outputUrl="/Users/yuanbao/Desktop"):
    # k个聚类中心
    data_points = read_data(url)
    assignment, end_sum_E, end_center, count = k_means(data_points, k)
    min_sum_E = 1000
    # 返回较小误差
    while min_sum_E > end_sum_E:
        min_sum_E = end_sum_E
        assignment, end_sum_E, end_center, count = k_means(data_points, k)
    result = print_result(count, min_sum_E, k, assignment)  # 输出结果
    plot(k, assignment, end_center, result, outputUrl)  # 画图


if __name__ == '__main__':
    a = []
    # 其中sys.argv用于获取参数url1，url2等。而sys.argv[0]代表python程序名，所以列表从1开始读取参数。
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    print(main(int(a[0]), a[1], a[2]))
# main()
