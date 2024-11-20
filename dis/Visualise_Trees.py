# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 15:23:21 2020

@author: Norman
"""
import sklearn.datasets as datasets
import pandas as pd
from sklearn.externals.six import StringIO 
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.tree import DecisionTreeClassifier

#NOTE This visualisation method works best in a jupyterLab or Jupyter notebook
#THis version of scikit-learn must be installed for the visualisation to work
!pip install --upgrade scikit-learn==0.20.3

#After the model is trained either call the model or paste this code below
#Because this is a random forest model 1 tree from the model is taken
estimator = WINA_rf.estimators_[1]
dot_data = StringIO()
export_graphviz(estimator, out_file=dot_data,feature_names = WINA_Features,  
                filled=True, rounded=True,class_names=['Draw','Win','Lose'],
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())