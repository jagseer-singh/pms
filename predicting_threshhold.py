# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:00:25 2020

@author: Jagseer Singh
"""

import datetime
import pickle
import pyodbc
from sklearn.preprocessing import PolynomialFeatures
def fnc():
    server = 'jagseer73.database.windows.net'
    database = 'pharmacy'
    username = 'root7'
    password = 'cse@18103060'
    driver= 'ODBC Driver 17 for SQL Server'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cu=cnxn.cursor()
    pro=[]
    for i in range(101,157):
        pro.append(i)
    with open('selling_predictor.pkl', 'rb') as file:
        Model = pickle.load(file)
    days=[]
    today=datetime.date.today()
    for i in range(1,8):
        temp=today - datetime.timedelta(days=i)
        days.append(temp)
    selling_data_x=[]
    cu.execute("Select * from selling_reports")
    temp=cu.fetchall()

    for i in pro:
        l=[]
        for j in days:
            l.append(0)
        selling_data_x.append(l)
    
    for i in temp:
        index=i[0]-101
        day=today-i[1]
        day=day.days
        if day<7:
            
            selling_data_x[index][7-day]+=i[2]
    

    polynomial_features = PolynomialFeatures(degree=2)
    x_poly = polynomial_features.fit_transform(selling_data_x)
    
    
    y_pred=Model.predict(x_poly)
    y_pred=y_pred.reshape(-1,1)
    for i in y_pred:
        if i[0]<30:
            i[0]=30
    
    val1=[]
    cu.execute("Select quantity,product_id from stock")
    st_q=cu.fetchall()
    qq=[0 for i in range(1,57)]
    for i in range(1,57):
        p_id=100+i
        th=int(y_pred[i-1][0])
        r=(p_id,th)
        val1.append(r)
    
    for i in st_q:
        st_q_p=i[1]
        index=st_q_p-101
        qq[index] += i[0]
    
    cu.executemany("update products set threshhold=? where product_id=?",val1)
    cnxn.commit()
    val2=[]
    for i in range(1,57):
        p_id=100+i
        quant=qq[i-1]
        tu=(quant,p_id)
        val2.append(tu)
    
    cu.executemany("update products set stock_present=? where product_id=?",val2)
    cnxn.commit()
