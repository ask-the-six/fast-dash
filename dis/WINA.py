# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import DataPrep
from DataPrep import Binary,Continuous,Discrete,Nominal, Ordinal, Targets,CutVars,Hours 
        
#%%

#One hot encoding for Categocial Variables
OrdinalDummy=pd.concat([pd.get_dummies(Ordinal[col]) for col in Ordinal], axis=1, keys=Ordinal.columns)
NominalDummy=pd.concat([pd.get_dummies(Nominal[col]) for col in Nominal], axis=1, keys=Nominal.columns)
#Battle outcomes used to train (assuming they can be predicted by other models)
FeatureTargets = Targets[['KMDA','CASA','CASD']].copy()

#%%
#Designate Target Variable
WINA_T1 = Targets['WINA']
#Create dataset to be trained on
X = pd.concat([Continuous, Discrete,NominalDummy,OrdinalDummy,FeatureTargets,WINA_T1], axis= 1)

#Remove rows or columns from the dataset here

#Drop battles with missing target variable
X = X.drop(X[X.WINA == -9].index)
#Designate Target Variable with removed battles gone
WINA_T1=X['WINA']


#Convert discrete variables to ratios
X['FEratio'] = X.CASA/ X.CASD
X = X.drop('CASA',1)
X = X.drop('CASD',1)


X['Fratio'] = X.STRA/ X.STRD
X = X.drop('STRA',1)
X = X.drop('STRD',1)

X['INratio'] = X.INTSTA /X.INTSTD 
X = X.drop('INTSTD',1)
X = X.drop('INTSTA',1)
#Separate target variable for training
X = X.drop('WINA',1)
#Create list of variables for use in NewBattlesPred
WINA_Features= list(X.columns.values)
#At this point any alterations to the prediction variables is done





#%%
#Turn the dataframe into an array
labels = np.array(WINA_T1)
feature_list = list(X.columns)
WINA_Features= feature_list 
features = np.array(X)
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 100)

#%%
from sklearn.ensemble import RandomForestClassifier
WINA_rf = RandomForestClassifier(n_estimators = 13172, random_state = 100,min_samples_split = 2, min_samples_leaf = 2, max_features = 'auto',
 max_depth = 58, bootstrap = False)
WINA_rf.fit(train_features, train_labels);
#%%
test_labels = test_labels.astype(np.float)
predictions = WINA_rf.predict(test_features)
errors = abs(predictions - test_labels)
print('Mean Error:', round(np.mean(errors), 2), 'degrees.')

#%%
importances = list(WINA_rf.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances];

#%%
from sklearn.metrics import confusion_matrix, classification_report

conf_mat = confusion_matrix(test_labels, predictions)
print(conf_mat)
print(classification_report(test_labels, predictions))

predictions.sum()

#%%

