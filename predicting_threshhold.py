# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 02:29:11 2020

@author: Jagseer Singh
"""

import datetime
import pickle
import pyodbc
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
    for i in range(1,5):
        temp=today - datetime.timedelta(days=i)
        days.append(temp)
    selling_data_x=[]
    for i in pro: # i is product_id
        l=[]
        for d in days: #d is selling date
            cmd=("Select quantity from selling_reports where product_id=? and selling_date=?")
            val=(i,d)
            cu.execute(cmd,val)
            temp=cu.fetchall()
            q=0
            for j in temp:
                q=q+j[0]
            l.append(q)
        selling_data_x.append(l)
    y_pred=Model.predict(selling_data_x)
    for i in range(1,57):
        p_id=100+i
        cmd=("update products set threshhold=? where product_id=?")
        val=(int(y_pred[i-1][0]),p_id)
        cu.execute(cmd,val)
        cnxn.commit()
        
        cmd=("Select quantity from stock where product_id=?")
        val=(p_id,)
        cu.execute(cmd,val)
        st=cu.fetchall()
        q_present=0
        for i in st:
            q_present=q_present+i[0]
        cmd="update products set stock_present=? where product_id=?"
        val=(q_present,p_id)
        cu.execute(cmd,val)
        cnxn.commit()
