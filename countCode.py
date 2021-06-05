# -*- coding: utf-8 -*-

"""
简易统计Python代码行数
"""


def count_code_nums(file):
    """
    :param file: 文件路径，.py文件
    :rtype :int
    """
    with open(file, encoding='utf-8') as data:
        count, flag = 0, 0
        begin = ('"""', "'''")
        for line in data:
            line2 = line.strip()
            if line2.startswith('#'):
                continue
            elif line2.startswith(begin):
                if line2.endswith(begin) and len(line2) > 3:
                    flag = 0
                    continue
                elif flag == 0:
                    flag = 1
                else:
                    flag = 0
                    continue
            elif flag == 1 and line2.endswith(begin):
                flag = 0
                continue
            if flag == 0 and line2:
                count += 1
    return count


def detect_rows(begin=0, root='.'):
    """
    统计指定文件夹内所有py文件代码量
    :param begin: 起始，一般使用默认0即可
    :param root: 需要统计的文件（文件夹）路径
    :rtype :int
    """
    import os, glob
    for file in glob.glob(os.path.join(root, '*')):
        if os.path.isdir(file):
            begin += detect_rows(0, file)
        elif file.endswith('.py'):
            begin += count_code_nums(file)
    return begin


if __name__ == '__main__':

    list_python_file_url = ['/Users/yuanbao/Desktop/kmeans算法/agglomerativeClustering.py',
                            '/Users/yuanbao/Desktop/kmeans算法/dbscan.py',
                            '/Users/yuanbao/Desktop/kmeans算法/gmm.py',
                            '/Users/yuanbao/Desktop/kmeans算法/KmeansPlus.py',
                            '/Users/yuanbao/Desktop/kmeans算法/kmeansPlus2.py',
                            '/Users/yuanbao/Desktop/kmeans算法/kmeansplusplus.py',
                            '/Users/yuanbao/Desktop/deeplearning/loadModel.py',
                            '/Users/yuanbao/Desktop/深度学习预测CPU资源的变化/forecastCpu2.py',
                            '/Users/yuanbao/Desktop/kmeans算法/countCode.py',
                            '/Users/yuanbao/Desktop/github/fileLoad/NeuralNetworks/NeuralNetworks/NeuralNerwork.py',
                            '/Users/yuanbao/Desktop/github/fileLoad/NeuralNetworks/NeuralNetworks/TestDic.py']
    count = 0
    for i in range(len(list_python_file_url)):
        print('文件'+str(i)+'纯代码量为:',count_code_nums(list_python_file_url[i]))
        count += count_code_nums(list_python_file_url[i])

    print("python脚本总的代码量为：",count)

