import matplotlib.pyplot as plt
from algorithm import *


# 手肘法
def SSE(filename):
    result = []
    for center_num in range(2, 10):
        min_loss = 10000
        for i in range(50):
            km_ = KM(filename, center_num)
            km_.init_center()
            km_.iter()
            loss = sum([i.min_distance for i in km_.point_matrix]) / len(km_.point_matrix)
            if loss < min_loss:
                min_loss = loss
        result.append(min_loss)
    print(result)


# 手肘法画图功能
def pic_SSE(SSE_result, savefile):
    fig = plt.figure(figsize=(10, 10), dpi=100)
    fig.plot(range(2, 11), SSE_result)
    fig.tight_layout()
    fig.savefig(savefile + ".svg")


# 聚类画图功能
def pic_km(km_, savefile):
    color_list = ['#4198b9', '#bbabd0', '#f2c494', '#91cfc9', '#e99a9a',
                  '#f26a21', '#ed1c24', '#007a67', '#fcc20e', '#f9bcbd']
    fig = plt.figure(figsize=(10, 10), dpi=100)
    for point in km_.point_matrix:
        if not point.cluster:
            fig.scatter(point.position, color='dimgray', marker='o')
        else:
            fig.scatter(point.position, color=color_list[point.cluster], marker='o')
    for center in km_.center_list:
        fig.scatter(center, color=color_list[point.cluster], marker='v')
    fig.tight_layout()
    fig.savefig(savefile + ".svg")