
#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from DataPrep import Binary,Continuous,Discrete,Nominal, Ordinal, Targets,CutVars,Cleaned_Dataset
#%%

cwd = os.getcwd()
cwd

#%%

X = pd.concat([Continuous, Discrete], axis= 1)
Y =Targets
XY = pd.concat([Y, X], axis= 1)


#%%

Plot1 =Y.hist(figsize=(20,10))
plt.show()

Plot2 =Y.plot.box(figsize=(20,10), subplots=True)
plt.show()

Plot3 =X.plot.box(figsize=(20,10), subplots=True)
plt.show()

#%%
f = plt.figure(figsize=(500, 200))
plt.matshow(XY.corr(), fignum=f.number)
plt.xticks(range(X.shape[1]), X.columns, fontsize=24, rotation=45)
plt.yticks(range(Y.shape[1]), Y.columns, fontsize=24)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=25)
plt.title('Correlation Matrix', fontsize=16);


#%%


#%%
X=Nominal
for i in X.columns:
    coll = i
    State_info = X.groupby(by=i)
    State_counts= State_info[i].count()
    uniqueV=X[i].unique() 
    labels = list(State_counts.index.values)
    colors = ['y','r','b','g','c','m']
    
    plt.pie(State_counts,labels =labels,colors = colors, autopct='%1.1f%%', startangle=0, pctdistance=.50)
    centre_circle = plt.Circle((0,0),0.8,fc='white')
    plt.gca().add_artist(centre_circle)
    plt.axis('off')
    plt.title(coll, y=1.00,fontweight='bold')
    #plt.savefig(str(i)+'1.png')
    plt.show()

#%%
 for i in ContinVar.columns:
    rowData = LiIndex.loc[ : , i ]
    rowData  = ' '.join(str(LiIndex[i].values))
    coll = i
    State_info = ContinVar.groupby(by=i)
    State_counts= State_info[i].count()
    uniqueV=ContinVar[i].unique() 
    labels = list(State_counts.index.values)
    colors = ['y','r','b','g','c','m']
    
    plt.pie(State_counts,labels =labels,colors = colors, autopct='%1.1f%%', startangle=0, pctdistance=.50)
    centre_circle = plt.Circle((0,0),0.8,fc='white')
    plt.gca().add_artist(centre_circle)
    plt.axis('off')
    plt.figtext(0, .01, rowData)
    plt.title(coll, y=1.00,fontweight='bold')
    #plt.savefig(str(i)+'1.png')
    plt.show()
    

#%%
State_info = CatVar.groupby("YR1")
print(State_info)
#%%
#"NOTES"

print(State_info)  
#"Prints count of uniqe values of colunmns
for i in KStart.columns:
    uniqueValues = KStart[i].nunique()
    print(uniqueValues)
    
#"This prints all the unique values in each column
  for i in CatVar.columns:
      uniqueV=CatVar[i].unique() 
      print(uniqueV)