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

js_code_str = '''
            function(params){
            return params.data.text;
            }
            '''

file_road = r'G:\LEARNING\Visualization_Project\static\datasets\009log_neat_square_225.npy'
km = KM(file_road, 9)


# km.init_center()
# km.iter()


def index(request):
    scatter = Scatter(init_opts=opts.InitOpts(width="500px", height="500px", theme=ThemeType.DARK))
    none_points, cluster_points = km.read_position()
    print(none_points.dtype)
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
    return render(request, 'visualization.html', {'pic': index(request)})
