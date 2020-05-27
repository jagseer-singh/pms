# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 03:48:22 2020

@author: Jagseer Singh
"""

import pandas as pd
import numpy as np
import pickle

Pkl_Filename = "selling_predictor.pkl"
dataset=pd.read_csv("dataset.csv")
x=dataset.iloc[:,0:7]
y=dataset.iloc[:,7].values
print(x.shape,y.shape)

from sklearn.preprocessing import PolynomialFeatures
polynomial_features = PolynomialFeatures(degree=2)
x_poly = polynomial_features.fit_transform(x)
print(x_poly.shape)

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x_poly,y,train_size=0.8)
print(x_train.shape,y_train.shape,y_test.shape)
from sklearn.linear_model import LinearRegression 
regr = LinearRegression()   
regr.fit(x_train, y_train) 
y_pred=regr.predict(x_test)
print(y_pred.shape)
print(y_pred)
print("Regresion Score:",regr.score(x_test,y_test))
with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(regr, file)



