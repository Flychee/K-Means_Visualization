import numpy as np
import copy
import random


# 迭代点类
class Point:
    def __init__(self, position):
        self.position = position
        self.cluster = None

    def choose_cluster(self, center_list):
        index = 0
        min_distance = np.inf
        for center in center_list:
            temp_result = np.linalg.norm(self.position, center)
            if temp_result < min_distance:
                min_distance = temp_result
                index = cluster_center_list.index(center)
        self.cluster = index


# 算法类
class KM:
    def __init__(self, filename, center_num):
        self.point_matrix = [Point(element) for element in np.load(filename)]  # 迭代点矩阵
        self.center_list = []  # 中心点
        self.center_num = center_num  # 中心点个数
        self.iter_limit = 10

    #  选取初始中心点
    def init_center(self):
        temp_matrix = copy.deepcopy(self.point_matrix)
        for _ in range(self.center_num):
            temp = random.choice(temp_matrix)
            self.center_list.append(temp.position)
            temp_matrix.remove(temp)

    # 更新函数
    def update(self):
        # 聚类更新
        pm_len = len(self.point_matrix)
        for num in range(pm_len):
            self.point_matrix[num].choose_cluster(self.center_list)

        # 中心点更新
        cl_len = len(self.center_list)
        for num in range(cl_len):
            temp_center = np.array([0, 0])
            point_num = 0
            for point in self.point_matrix:
                if point.cluster == num:
                    temp_center += point.position
                    point_num += 1
            temp_center /= point_num
            self.center_list[num] = temp_center
