
import pandas as pd
import seaborn as sns
import numpy as np
import os
import DataPrep
from DataPrep import Binary,Continuous,Discrete,Nominal, Ordinal, Targets,CutVars

#%%
#One hot encoding for Categocial Variables
OrdinalDummy=pd.concat([pd.get_dummies(Ordinal[col]) for col in Ordinal], axis=1, keys=Ordinal.columns)
NominalDummy=pd.concat([pd.get_dummies(Nominal[col]) for col in Nominal], axis=1, keys=Nominal.columns)
FeatureTargets = Targets[['CASA','CASD']].copy() # Training this model with data that should aleady be predicted
#%%
#Removal variables- Binary
ACHA_T1=Targets['ACHA'] 
X = pd.concat([Binary,Continuous, Discrete,NominalDummy,OrdinalDummy,FeatureTargets,ACHA_T1], axis= 1)
#Insert more filters here if needed
ACHA_T1=X['ACHA'] 

X = X.drop('ACHA',1)
X=X.apply(pd.to_numeric)
ACHA_Features= list(X.columns.values)
#At this point any alterations to the prediction variables is done

#Creating the dependent variable class
Labels = pd.factorize(ACHA_T1)
#%%
labels = np.array(ACHA_T1)

labels = labels.astype(np.float)
labels=labels+1
feature_list = list(X.columns)
features = np.array(X)
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 100)


#%%
from sklearn.ensemble import RandomForestRegressor
ACHA_rf = RandomForestRegressor(n_estimators = 1000, random_state = 100)
ACHA_rf.fit(train_features, train_labels);
#%%
test_labels = test_labels.astype(np.float)
predictions = ACHA_rf.predict(test_features)
errors = abs(predictions - test_labels)
print('Mean Error:', round(np.mean(errors), 2), 'on scale of 0-9.')


#%%
importances = list(ACHA_rf.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances];
#%%
