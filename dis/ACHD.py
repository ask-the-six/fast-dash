import pandas as pd
import seaborn as sns
import numpy as np
import os
import DataPrep
from DataPrep import Binary,Continuous,Discrete,Nominal, Ordinal, Targets,CutVars
#%%

#%%
        #One hot encoding for Categocial Variables
OrdinalDummy=pd.concat([pd.get_dummies(Ordinal[col]) for col in Ordinal], axis=1, keys=Ordinal.columns)
NominalDummy=pd.concat([pd.get_dummies(Nominal[col]) for col in Nominal], axis=1, keys=Nominal.columns)
FeatureTargets = Targets[['CASA','CASD']].copy()
#%%
#Removal variables- 
ACHD_T1=Targets['ACHD'] 
X = pd.concat([Binary,Continuous, Discrete,NominalDummy,OrdinalDummy,FeatureTargets,ACHD_T1], axis= 1)
#Insert more filters here if needed


ACHD_T1=X['ACHD'] 

X = X.drop('ACHD',1)
X=X.apply(pd.to_numeric)
ACHD_Features= list(X.columns.values)



#At this point any alterations to the prediction variables is done
#Creating the dependent variable
Labels = pd.factorize(ACHD_T1)

#%%
labels = np.array(ACHD_T1)

labels = labels.astype(np.float)
labels=labels+1
feature_list = list(X.columns)
features = np.array(X)
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 100)


#%%
from sklearn.ensemble import RandomForestRegressor
ACHD_rf = RandomForestRegressor(n_estimators = 1000, random_state = 100)
ACHD_rf.fit(train_features, train_labels);
#%%
test_labels = test_labels.astype(np.float)
predictions = ACHD_rf.predict(test_features)
errors = abs(predictions - test_labels)
print('Mean Error:', round(np.mean(errors), 2), 'degrees.')

#%%
importances = list(ACHD_rf.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances];
#%%
from sklearn import metrics

[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances];
print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(test_labels, predictions))
print('Mean Squared Error (MSE):', metrics.mean_squared_error(test_labels, predictions))
print('Root Mean Squared Error (RMSE):', np.sqrt(metrics.mean_squared_error(test_labels, predictions)))
mape = np.mean(np.abs((test_labels - predictions) / np.abs(test_labels)))
print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
print('Accuracy:', round(100*(1 - mape), 2))