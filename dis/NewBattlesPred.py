# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:18:05 2020

@author: Norman
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

os.chdir("C:/Users/Norman/Desktop/Test") #Set to location of saved files
cwd = os.getcwd()
cwd
import DataPrep #This is the DataPrep.py file that prepares the original dataset for training
from DataPrep import CutVars

#%%


KStart= pd.read_csv("NewBattles.csv", thousands=',') #"The Battles to be predicted

#%% The following blocks of code categorize the variables so they can be modified to increase prediction accuracy
#This removes the variables Determined to not be used for prediction
X = CutVars['Remove'] == "Remove " #Create variable to determine removal status
Y=CutVars[X] #New DF with only removeable variables
X=Y['Nomen'].tolist() #Creates list of names of columns
Cut2=CutVars[CutVars.Remove != 'Remove ']#This Creates the Dataframe for the next segment removing the variables that have been segmented
Cleaned=KStart.drop(columns= X, axis=1)

X = Cut2['Label'] == "Battle Outcomes" 
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Cut2=Cut2[Cut2.Label != 'Battle Outcomes']
Targets=Cleaned[X]
Targets = Targets.replace(',','', regex=True)
Targets.name = 'Targets'


X = Cut2['Subtype'] == "Ordinal" 
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Ordinal=Cleaned[X]


X = Cut2['Label'] == "Influence" 
Y=Cut2[X]
X=Y['Nomen'].tolist()
Ordinal = Ordinal.drop(X,axis='columns')
Ordinal = Ordinal.drop(['CODEA', 'CODED'],axis='columns')
Ordinal.name = 'Ordinal'

X = Cut2['Subtype'] == "Discrete" 
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Discrete=Cleaned[X]
Discrete = Discrete.replace(',','', regex=True) #Replaces Commas 
Discrete.name ='Discrete'

X = Cut2['Subtype'] == "Nominal"
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Nominal=Cleaned[X]
Nominal = Nominal.drop(['ENGAGEMENT NAME','CAMPAIGN', 'ATTACKING COMMANDER', 'DEFENDING COMMANDER',	'LOCATION',	'NAME OF ATTACKING FORCE', 'NAME OF DEFENDING FORCE', 'WAR NAME'] , axis='columns')
Nominal.name= 'Nominal'

X = Cut2['Subtype'] == "Continuous" 
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Continuous=Cleaned[X]
Continuous = Continuous.drop(['CASAMI',	'CASAPL', 'CASDMI', 'CASDPL', 'STRAMI', 'STRAPL', 'STRDMI', 'STRDPL'] , axis='columns') #Drops Error values plus/minus
Continuous.name = 'Continuous'

X = Cut2['Subtype'] == "Binary" 
Y=Cut2[X] 
X=Y['Nomen'].tolist()
Binary=Cleaned[X]
Binary.name = 'Binary'


#%%
#One hot encoding for Categocial Variables


Nominal = Nominal.drop(columns=['WX1', 'WX2', 'PRIA1','TERRA1', 'TERRA2','POST1','PRID2'])
Ordinal = Ordinal.drop(columns=['TECHA', 'LOGSA','CEA'])

OrdinalDummy=pd.concat([pd.get_dummies(Ordinal[col]) for col in Ordinal], axis=1, keys=Ordinal.columns)
NominalDummy=pd.concat([pd.get_dummies(Nominal[col]) for col in Nominal], axis=1, keys=Nominal.columns)

 
 
 
 #%% FINSTD Predictions
from FINSTD import FINSTD_Features, FINSTD_rf 
X= pd.concat([Continuous, Discrete,NominalDummy,OrdinalDummy], axis= 1)
X=X.apply(pd.to_numeric)
FINSTD_DF = pd.DataFrame(columns = FINSTD_Features)
merged_X = pd.concat([FINSTD_DF,X],axis=0, ignore_index=True ,sort=False) #This matches the columns with the code 
merged_X = merged_X.fillna(0)
FINSTD_Features  = np.array(merged_X)
FINSTD_Preds = FINSTD_rf.predict(FINSTD_Features)

  #%% FINSTA Predictions
from FINSTA import  FINSTA_Features, FINSTA_rf 
X= pd.concat([Continuous, Discrete,NominalDummy,OrdinalDummy], axis= 1)
X=X.apply(pd.to_numeric)
FINSTA_DF = pd.DataFrame(columns = FINSTA_Features)
merged_X = pd.concat([FINSTA_DF,X],axis=0, ignore_index=True ,sort=False) #This matches the columns with the code 
merged_X = merged_X.fillna(0)
FINSTA_Features  = np.array(merged_X)
FINSTA_Preds = FINSTA_rf.predict(FINSTD_Features)

    


#%% WINA Predictions
from WINA import WINA_Features, WINA_rf
CASAFinal = pd.DataFrame(Discrete['STRA']- FINSTA_Preds)
CASDFinal = pd.DataFrame(Discrete['STRD']- FINSTD_Preds)
CASDFinal.columns = ['CASD']
CASAFinal.columns = ['CASA']

X = pd.concat([Continuous, Discrete,NominalDummy,OrdinalDummy,CASAFinal,CASDFinal], axis= 1)


X['FEratio'] = X.CASA/ X.CASD
X = X.drop('CASA',1)
X = X.drop('CASD',1)


X['Fratio'] = X.STRA/ X.STRD
X = X.drop('STRA',1)
X = X.drop('STRD',1)

X['INratio'] = X.INTSTA /X.INTSTD 
X = X.drop('INTSTD',1)
X = X.drop('INTSTA',1)


X=X.apply(pd.to_numeric)

WINA_DF = pd.DataFrame(columns = WINA_Features)
merged_X = pd.concat([WINA_DF,X],axis=0, ignore_index=True ,sort=False) 
merged_X = merged_X.fillna(0)
merged_X1  = np.array(merged_X)
WINA_Preds = WINA_rf.predict(merged_X1)
#%% This creates a .csv file containing the predictions for the new battles that is saved in the directory 
Names= KStart['ENGAGEMENT NAME']
Predictions = {'Battle Scenerio':Names,'FINSTD':FINSTD_Preds,'FINSTA':FINSTA_Preds,'WINA':WINA_Preds, 'Casualties Attacker':CASAFinal['CASA'], 'CASD':CASDFinal['CASD']} 
Predictions =pd.DataFrame(Predictions)
Predictions.to_csv('Predictions.csv',encoding='utf-8', index=False,header=True)
#%%
