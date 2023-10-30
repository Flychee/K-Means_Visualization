import matplotlib
from algorithm import *


# 手肘法
def SSE(filename):
    result = []
    for center_num in range(2, 10):
        min_loss = 10000
        for i in range(50):
            km = KM(filename, center_num)
            km.init_center()
            km.iter()
            loss = sum([i.min_distance for i in km.point_matrix]) / len(km.point_matrix)
            if loss < min_loss:
                min_loss = loss
        result.append(min_loss)
    print(result)
