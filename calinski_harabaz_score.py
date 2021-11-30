from sklearn import mixture
from sklearn import metrics
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Z_ScoreNormalization(x, mu, sigma):
    x = (x - mu) / sigma
    return x


def test_GMM(dataMat, components, iter=100, cov_type="full"):
    clst = mixture.GaussianMixture(n_components=components, max_iter=iter, covariance_type=cov_type)
    clst.fit(dataMat)
    predicted_labels = clst.predict(dataMat)
    return clst.means_, predicted_labels


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
data = np.array(mdl[['longitude', 'latitude', '2020population', '2020gdp', '2020LuminousIndex', '2020populationper', '2019ElectricityConsumpionpergdp']])
dataMat = Z_ScoreNormalization(data, data.mean(), data.std())
print(dataMat)

cluster_num = range(2, 7)
score_all = []
for k in cluster_num:
    n_components = k
    iter = 100
    cov_types = ['spherical', 'tied', 'diag', 'full']
    centroids, labels = test_GMM(dataMat, n_components, iter, cov_types[3])
    mdl['label'] = labels
    score = metrics.calinski_harabasz_score(dataMat, labels)
    score_all.append(score)

plt.plot(cluster_num, score_all)
plt.show()