import xlrd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


rawData = xlrd.open_workbook('./data/rawcitydata2的副本.xlsx')
table = rawData.sheets()[0]
data = []
for i in range(table.nrows):
    if i == 0:
        continue
    else:
        data.append(table.row_values(i)[0:])

featureList = ['city', 'longitude', 'latitude', '2020population', '2020gdp', '2020LuminousIndex', '2020populationper', '2019ElectricityConsumpionpergdp']
mdl = pd.DataFrame.from_records(data, columns=featureList)
print(mdl)


mdl_new = np.array(mdl[['longitude', 'latitude', '2020population', '2020gdp', '2020LuminousIndex', '2020populationper', '2019ElectricityConsumpionpergdp']])
seed = 0  # 设置随机数
clf = KMeans(n_clusters=2, random_state = seed, init = "k-means++")  # 聚类
clf.fit(mdl_new)

print(clf.cluster_centers_)

mdl['label'] = clf.labels_ #对原数据表进行类别标记
print(mdl)

#city_list = mdl.loc[:,'city'].tolist()
#label_list = mdl.loc[:,'label'].tolist()


from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
c = (
    Geo(init_opts=opts.InitOpts(width="1400px", height="700px", theme='dark'))  # 图表大小, 主题风格
        .add_schema(maptype="china",  # 地图
                    itemstyle_opts=opts.ItemStyleOpts(color="#28527a",  # 背景颜色
                                                      border_color="#9ba4b4"))  # 边框颜色, 可在 https://colorhunt.co/选择颜色
        .add(
        "",  # 系列名称, 可不设置
        [(i, j) for i, j in zip(mdl['city'], mdl['label'])],  # 数据
        type_=ChartType.EFFECT_SCATTER,  # 涟漪散点
        effect_opts=opts.EffectOpts(symbol_size=1),  # 标记大小
    )

        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示标签
        .set_global_opts(title_opts=opts.TitleOpts(title="全国地级市聚类图",  # 图表标题
                                                   pos_left='center',  # 标题位置
                                                    ),
                         visualmap_opts=opts.VisualMapOpts(max_= 1,
                                                           range_text=['CityType', ''],  # 上下的名称
                                                           split_number=4,  # 如果是连续数据, 分成几段
                                                           pos_left='20%',  # pos_right
                                                           pos_top='70%',  # pos_bottom
                                                           is_piecewise=True,  # 是否为分段显示
                                                           pieces=[
                                                               {"min": 1, "max": 1, "color": "#32e0c4", 'label': '1'},
                                                               {"min": 0, "max": 0, "color": "#b8de6f", 'label': '0'},
                                                               ])))

c.render("./kmeansCityClustering.html")