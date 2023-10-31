from django.shortcuts import render, HttpResponse
import numpy as np
import copy
import random


# 迭代点类
class Point:
    def __init__(self, position):
        self.position = position
        self.min_distance = np.inf
        self.cluster = None

    def choose_cluster(self, center_list):
        for index, center in enumerate(center_list):
            temp_distance = np.linalg.norm(self.position - center)
            if temp_distance < self.min_distance:
                self.min_distance = temp_distance
                self.cluster = index


# 算法类
class KM:
    def __init__(self, filename, center_num):
        self.point_matrix = [Point(element) for element in np.load(filename)]  # 迭代点矩阵
        self.center_list = []  # 中心点
        self.center_num = center_num  # 中心点个数
        self.iter_limit = 20  # 迭代次数上限

    #  选取初始中心点
    def init_center(self):
        temp_matrix = copy.deepcopy(self.point_matrix)
        for _ in range(self.center_num):
            temp = random.choice(temp_matrix)
            self.center_list.append(temp.position)
            temp_matrix.remove(temp)

    #  读取坐标
    def read_position(self):
        result = []
        for point in self.point_matrix:
            result.append(point.position)
        return result

    def read_cluster(self):
        result = []
        for point in self.point_matrix:
            result.append(point.cluster)
        return result

    # 更新函数
    def update(self):
        # 聚类更新
        pm_len = len(self.point_matrix)
        for index in range(pm_len):
            self.point_matrix[index].choose_cluster(self.center_list)
        # 中心点更新
        cl_len = len(self.center_list)
        for index in range(cl_len):
            temp_center = np.array([0, 0], dtype='float64')
            point_num = 0
            for point in self.point_matrix:
                if point.cluster == index:
                    temp_center += point.position
                    point_num += 1
            if point_num != 0:
                temp_center /= point_num
                self.center_list[index] = temp_center

    # 迭代函数
    def iter(self):
        balance_bool = False
        num = 0
        while not balance_bool or num < self.iter_limit:
            temp_matrix = copy.deepcopy(self.point_matrix)
            self.update()
            for temp, point in zip(temp_matrix, self.point_matrix):
                balance_bool = True if temp.cluster == point.cluster else False
            num += 1


# Create your views here.
def test(request):
    road_file = 'static/datasets/001log_uniform_200.npy'
    km = KM(road_file, 4)
    stri = str(km.read_position())
    return HttpResponse(stri)