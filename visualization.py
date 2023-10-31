import matplotlib
import matplotlib.pyplot as plt
from algorithm import *


# 手肘法
def SSE(filename):
    result = []
    for center_num in range(2, 11):
        min_loss = 10000
        for i in range(10):
            km_ = KM(filename, center_num)
            km_.init_center()
            km_.iter()
            loss = sum([i.min_distance for i in km_.point_matrix]) / len(km_.point_matrix)
            if loss < min_loss:
                min_loss = loss
        result.append(min_loss)
    return result


# 手肘法画图功能
def pic_SSE(SSE_result, savefile):
    plt.figure(figsize=(10, 7), dpi=100)
    plt.plot(range(2, len(SSE_result) + 2), SSE_result)
    plt.tight_layout()
    # plt.savefig(savefile + ".svg")
    plt.show()


# 聚类画图功能
def pic_km(km_, savefile):
    color_list = ['#4198b9', '#bbabd0', '#f2c494', '#91cfc9', '#e99a9a',
                  '#f26a21', '#ed1c24', '#007a67', '#fcc20e', '#f9bcbd']
    plt.figure(figsize=(10, 10), dpi=100)
    for point in km_.point_matrix:
        if point.cluster is None:
            plt.scatter(point.position[0], point.position[1], color='dimgray', marker='o', s=50)
        else:
            plt.scatter(point.position[0], point.position[1], color=color_list[point.cluster], marker='o', s=50)
    for index, center in enumerate(km_.center_list):
        plt.scatter(center[0], center[1], color=color_list[index], marker='v', s=240)
    plt.tight_layout()
    # plt.savefig(savefile + ".svg")
    plt.show()


read_file = r'G:\LEARNING\K-Means_Visualization\Agents-200\001log_uniform_200.npy'

km = KM(read_file, 10)
km.init_center()
km.iter()
# print(km.read_cluster())
pic_km(km, 'test')

# pic_SSE(SSE(read_file), 'test')
