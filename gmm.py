from sklearn import mixture
import xlrd
import pandas as pd
import numpy as np

def Z_ScoreNormalization(x,mu,sigma):
    x = (x - mu) / sigma
    return x

def test_GMM(dataMat, components=2, iter = 100, cov_type="full"):
    clst = mixture.GaussianMixture(n_components=components,max_iter=iter,covariance_type=cov_type)
    clst.fit(dataMat)
    predicted_labels =clst.predict(dataMat)
    return clst.means_, predicted_labels

rawData = xlrd.open_workbook('./data/citydata.xlsx')
table = rawData.sheets()[0]
data = []
for i in range(table.nrows):
    if i == 0:
        continue
    else:
        data.append(table.row_values(i)[0:])

featureList = ['city', 'longtitude', 'latitude', '2019precipitation','2020gdp']
mdl = pd.DataFrame.from_records(data, columns=featureList)
data = np.array(mdl[['longtitude', 'latitude', '2019precipitation', '2020gdp']])
dataMat = Z_ScoreNormalization(data, data.mean(), data.std())
print(dataMat)

n_components = 2
iter = 100
cov_types = ['spherical', 'tied', 'diag', 'full']
centroids,labels = test_GMM(dataMat, n_components, iter, cov_types[3])
mdl['label'] = labels
print(mdl)

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType

c = (
    Geo(init_opts=opts.InitOpts(width="1400px", height="700px", theme='dark'))  # 图表大小, 主题风格
        .add_schema(maptype="china",  # 地图
                    itemstyle_opts=opts.ItemStyleOpts(color="#28527a",  # 背景颜色
                                                      border_color="#9ba4b4"))  # 边框颜色
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

c.render("./GMM全国地级市聚类图.html")