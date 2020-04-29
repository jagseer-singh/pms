# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:28:00 2020

@author: Jagseer Singh
"""

import datetime   
import mysql.connector
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import yaml
def fnc():
    Pkl_Filename = "selling_predictor.pkl"
    db=yaml.load(open('db.yaml'))
    mydb=mysql.connector.connect(
        host=db['mysql_host'],
        username=db['mysql_user'],
        passwd=db['mysql_password'],
        database=db['mysql_db'])
    cu=mydb.cursor()
    pro=[]
    for i in range(101,157):
        pro.append(i)	
    today=datetime.date.today()
    days_x=[]
    days_y=[]
    for i in range(1,7):
        if i<3:
            temp=today - datetime.timedelta(days=i)
            days_y.append(temp)
        else:
            temp=today - datetime.timedelta(days=i)
            days_x.append(temp)
    print(len(days_x))
    selling_data_x=[]
    selling_data_y=[]
    for i in pro: # i is product_id
        l=[]
        for d in days_x: #d is selling date
            cu.execute("Select quantity from selling_reports where product_id=%s and selling_date=%s",(i,d))
            temp=cu.fetchall()
            q=0
            for j in temp:
                q=q+j[0]
            l.append(q)
        selling_data_x.append(l)
        q_y=0
        for d in days_y: #d is selling date
            cu.execute("Select quantity from selling_reports where product_id=%s and selling_date=%s",(i,d))
            temp=cu.fetchall()
            for j in temp:
                q_y=q_y+j[0]
        y_temp=[q_y]
        selling_data_y.append(y_temp)
    x_train,x_test,y_train,y_test=train_test_split(selling_data_x,selling_data_y,train_size=0.8)
    regr = LinearRegression()   
    regr.fit(x_train, y_train)
    print(x_test)
    y_pred=regr.predict(x_test)
    print(y_pred)
    with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(regr, file)
fnc()
