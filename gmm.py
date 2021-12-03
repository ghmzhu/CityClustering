from sklearn import mixture
import xlrd
import pandas as pd
import numpy as np
import drawing


def test_GMM(dataMat, components=5, iter=100, cov_type="full"):
    clst = mixture.GaussianMixture(n_components=components, max_iter=iter, covariance_type=cov_type, reg_covar=1e-2)
    clst.fit(dataMat)
    predicted_labels =clst.predict(dataMat)
    return clst.means_, predicted_labels

rawData = xlrd.open_workbook('./data/rawcitydata.xlsx')
table = rawData.sheets()[0]
data = []
for i in range(table.nrows):
    if i == 0:
        continue
    else:
        data.append(table.row_values(i)[0:])

featureList = ['city', '2020LuminousIndex', '2020GDP', '2020Population', '2020PopulationperAdministrativeArea', '2020GDPperCapita', '2020PopulationAttractionIndex', '2019ElectricityConsumpionperGDP', '2019LocalGeneralPublicBudgetExpenditure', '2019ExpenditureforScienceandTechnology', '2019ExpenditureforEducation']
mdl = pd.DataFrame.from_records(data, columns=featureList)
dataMat = np.array(mdl[['2020LuminousIndex', '2020GDP', '2020Population', '2020PopulationperAdministrativeArea', '2020GDPperCapita', '2020PopulationAttractionIndex', '2019ElectricityConsumpionperGDP', '2019LocalGeneralPublicBudgetExpenditure', '2019ExpenditureforScienceandTechnology', '2019ExpenditureforEducation']])
print(dataMat)

n_components = 5
iter = 100
cov_types = ['spherical', 'tied', 'diag', 'full']
centroids, labels = test_GMM(dataMat, n_components, iter, cov_types[3])
mdl['label'] = labels
print(mdl)


drawing.plot(mdl)