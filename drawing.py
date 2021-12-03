from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType

def plot(df):
    c = (
        Geo(init_opts=opts.InitOpts(width="1400px", height="700px", theme='dark'))  # 图表大小, 主题风格
            .add_schema(maptype="china",  # 地图
                        itemstyle_opts=opts.ItemStyleOpts(color="#28527a",  # 背景颜色
                                                          border_color="#9ba4b4"))  # 边框颜色
            .add(
            "",  # 系列名称, 可不设置
            [(i, j) for i, j in zip(df['city'], df['label'])],  # 数据
            type_=ChartType.EFFECT_SCATTER,  # 涟漪散点
            effect_opts=opts.EffectOpts(symbol_size=1),)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示标签,formatter='{b}'
            .set_global_opts(title_opts=opts.TitleOpts(title="全国地级市聚类图",  # 图表标题
                                                       pos_left='center',  # 标题位置
                                                       ),
                             visualmap_opts=opts.VisualMapOpts(max_=1,
                                                               range_text=['CityType', ''],  # 上下的名称
                                                               split_number=4,  # 如果是连续数据, 分成几段
                                                               pos_left='20%',  # pos_right
                                                               pos_top='70%',  # pos_bottom
                                                               is_piecewise=True,  # 是否为分段显示
                                                               pieces=[
                                                                   {"min": 4, "max": 4, "color": "#ffff00",
                                                                    'label': '4'},
                                                                   {"min": 3, "max": 3, "color": "#32CD32",
                                                                    'label': '3'},
                                                                   {"min": 2, "max": 2, "color": "#1E90FF",
                                                                    'label': '2'},
                                                                   {"min": 1, "max": 1, "color": "#32e0c4",
                                                                    'label': '1'},
                                                                   {"min": 0, "max": 0, "color": "#9e5523",
                                                                    'label': '0'},
                                                               ])))

    c.render("./GMMCityClustering.html")
