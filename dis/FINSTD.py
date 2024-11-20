# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:12:58 2020

@author: Norman
"""
import pandas as pd
import numpy as np
import DataPrep
from DataPrep import Binary,Continuous,Discrete,Nominal, Ordinal, Targets,CutVars,Year
#%%
#One hot encoding for Categocial Variables

FINSTD_OrdinalDummy=pd.concat([pd.get_dummies(Ordinal[col]) for col in Ordinal], axis=1, keys=Ordinal.columns)
FINSTD_NominalDummy=pd.concat([pd.get_dummies(Nominal[col]) for col in Nominal], axis=1, keys=Nominal.columns)
#%%
FINSTD_T1=Targets['FINSTD']
X = pd.concat([Continuous, Discrete,FINSTD_NominalDummy,FINSTD_OrdinalDummy,FINSTD_T1,Year], axis= 1)
#%% Filters can Be added here to refine the model. They must also be added to the NewBattlesPred.py corresponding to this prediction
#Drop rows here that have missing variables

X = X.drop(X[X.Year < 1900 ].index)
X = X.drop(X[X.STRA > 20000 ].index)
X = X.drop(X[X.FINSTD == -1].index)
X = X.drop(X[X.FINSTD == 0].index)
FINSTD_T1=X['FINSTD']

X = X.drop('Year',1)
X = X.drop('FINSTD',1)
FINSTD_Features= list(X.columns.values)
#%%

labels = np.array(FINSTD_T1)  
feature_list = list(X.columns)
features = np.array(X)
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 100)


#%%
from sklearn.ensemble import RandomForestRegressor
FINSTD_rf = RandomForestRegressor(n_estimators = 1000, random_state = 100)
FINSTD_rf.fit(train_features, train_labels);
#%%
test_labels = test_labels.astype(np.float)
predictions = FINSTD_rf.predict(test_features)
errors = abs(predictions - test_labels)
print('Mean Error:', round(np.mean(errors), 2), 'Units')
#%%
importances = list(FINSTD_rf.feature_importances_)
feature_importances = [(feature, round(importance,3)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances];
#%%
from sklearn import metrics

print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(test_labels, predictions))
print('Mean Squared Error (MSE):', metrics.mean_squared_error(test_labels, predictions))
print('Root Mean Squared Error (RMSE):', np.sqrt(metrics.mean_squared_error(test_labels, predictions)))
mape = np.mean(np.abs((test_labels - predictions) / np.abs(test_labels)))
print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
print('Accuracy:', round(100*(1 - mape), 2))
np.set_printoptions(formatter={'float_kind':'{:f}'.format})
predictions - test_labels
test_features
pressss = predictions
Actual = test_labels
