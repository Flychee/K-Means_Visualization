from django.shortcuts import render
from algorithm.views import *
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./picture/templates"))
from pyecharts import options as opts
from pyecharts.charts import Scatter, EffectScatter
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

file_road_list = ['img/' + str(i) + '.png' for i in range(1, 11)]
datasets_road = {}
for i in range(1, 11):
    datasets_road.update({'img/' + str(i) + '.png': 'datasets/' + str(i) + '.npy'})
file_road = r'G:\LEARNING\Visualization_Project\static\datasets\009log_neat_square_225.npy'
km = KM(9)


# km.init_center()
# km.iter()

# 通过图片选取矩阵
def choose(request):
    if request.method == 'POST' and 'pic_road' in request.POST:
        km.init_matrix('static/' + datasets_road[request.POST['pic_road']])
    return render(request, 'visualization.html', {'pic': picture(request), 'file_road_list': file_road_list})


# 算法可视化
def picture(request):
    init_center_point = '初始化中心点'
    update_point = '迭代一次'
    iter_point = '迭代至最终结果'
    if request.method == 'POST' and 'func' in request.POST:
        point = request.POST['func']
        if point == init_center_point:
            km.init_center()
        elif point == update_point:
            km.update()
        elif point == iter_point:
            km.iter()

    scatter = Scatter(init_opts=opts.InitOpts(width="500px", height="500px", theme=ThemeType.DARK))
    none_points, cluster_points = km.read_position()
    # 描绘散点图
    if len(none_points) > 0:
        scatter.add_xaxis(xaxis_data=none_points.T[0])
        scatter.add_yaxis('None', none_points.T[1], color='gray')
    for item, cps in enumerate(cluster_points):
        if len(cps) > 0:
            scatter.add_xaxis(xaxis_data=cps.T[0])
            scatter.add_yaxis(str(item), cps.T[1])

    # 层叠中心点
    ef_scatter = EffectScatter()
    if len(km.center_list) > 0:
        for item, center in enumerate(km.center_list):
            ef_scatter.add_xaxis(xaxis_data=[center[0]])
            ef_scatter.add_yaxis(str(item), [center[1]], symbol_size=15)
    ef_scatter.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    ef_scatter.set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False))

    scatter.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    scatter.set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False),
                            legend_opts=opts.LegendOpts(pos_left='center',
                                                        pos_top='bottom', ),
                            xaxis_opts=opts.AxisOpts(max_=5,
                                                     min_=-5),
                            yaxis_opts=opts.AxisOpts(max_=5,
                                                     min_=-5)
                            )

    scatter.overlap(ef_scatter)
    return HttpResponse(scatter.render_embed())


def open_visualization(request):
    print(request.POST)
    return render(request, 'visualization.html', {'pic': picture(request), 'file_road_list': file_road_list})
