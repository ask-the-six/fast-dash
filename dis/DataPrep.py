import os
import pandas as pd




def df_var_meta(path: str="Variable_Table.csv")->pd.DataFrame:
    return pd.read_csv(path)

def historical_data(path: str="cdb91g.csv"):
    , thousands=','

KStart= pd.read_csv() #"The original dataset" thousands=',' Tells pandas to remove the , this is important to keep the data clean


#%%
#This is the First opportunity to drop and filter the dataset based on what variables you would like the model to look at. 
#To apply Filter delete the '#' symbol in front of it. 
#This will apply to all models

#BN 1000 Soldiers BDE 5000 Corps 20,000-45,000

#The below line will drop any battles dated before the date indicated
#KStart = KStart.drop(KStart[KStart.ATPEYR1 <1900 ].index) #Drop Before
#KStart = KStart.drop(KStart[KStart.ATPEYR1 >1900 ].index) #After
#KStart = KStart.drop(KStart[KStart.TRNGA == -9 ].index)
#KStart = KStart.drop(KStart[KStart.Days != 0 ].index)
#KStart = KStart.drop(KStart[KStart.Hours != 0 ].index)
#The following codes will filter based on size of the attacking forces
#BN 1000 Soldiers BDE 5000 Corps 20,000-45,000
#KStart = KStart.drop(KStart[KStart.STRA > 20000 ].index) #Less than 2000 (Battalion and below)
#KStart = KStart.drop(KStart[KStart.STRA > 20000 ].index) #Less than 20K BDE and below 
#KStart = KStart.drop(KStart[KStart.STRA < 20000.0 ].index) #Greater than 20K Corps and Higher


#KStart = KStart.drop(KStart[KStart.RERPA== -1].index)  b
#KStart = KStart.drop(KStart[KStart.WINA == -9].index)
#KStart = KStart.drop(KStart[KStart.CASD == "-1"].index)
#KStart['STRA']=KStart['STRA'].astype(float)
#%%
#This removes the variables Determined to not be used for Analysis in the Variable table
Year= pd.DataFrame(KStart['ATPEYR1'])
Year.columns = ['Year'] #This creates year filters that can be used by the target prediction models
Hours= pd.DataFrame(KStart['Hours'])
 #This creates year filters that can be used by the target prediction models


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
Discrete = Discrete.replace(',','', regex=True) 
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

Cleaned_Dataset = pd.concat([Binary,Continuous, Discrete,Nominal,Ordinal,Targets], axis= 1)
Nominal = Nominal.drop(columns=['WX1', 'WX2', 'PRIA1','TERRA1', 'TERRA2','POST1','PRID2'])
Ordinal = Ordinal.drop(columns=['TECHA', 'LOGSA','CEA'])
#%%


