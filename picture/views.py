from django.shortcuts import render
from algorithm.views import *
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./picture/templates"))
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

js_code_str = '''
            function(params){
            return params.data.text;
            }
            '''

file_road = r'G:\LEARNING\Visualization_Project\static\datasets\001log_uniform_200.npy'
km = KM(file_road, 3)
km.init_center()
km.update()


def index(request):
    scatter = Scatter(init_opts=opts.InitOpts(width="500px", height="500px"))
    none_points, cluster_points = km.read_position()
    if len(none_points) > 0:
        scatter.add_xaxis(xaxis_data=none_points.T[0])
        scatter.add_yaxis('None', none_points.T[1])
    for item, cps in enumerate(cluster_points):
        if len(cps) > 0:
            scatter.add_xaxis(xaxis_data=cps.T[0])
            scatter.add_yaxis(str(item), cps.T[1])
    scatter.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    scatter.set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False))
    return HttpResponse(scatter.render_embed())
