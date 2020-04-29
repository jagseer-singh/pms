# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 08:50:45 2020

@author: Jagseer Singh
"""
import pyodbc
server = 'jagseer73.database.windows.net'
database = 'pharmacy'
username = 'root7'
password = 'cse@18103060'
driver= 'ODBC Driver 17 for SQL Server'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cu=cnxn.cursor()

import datetime
import random

order_id=0
start_date = datetime.date(2020, 2,1)
end_date = datetime.date(2020, 4,1)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

pro=[]
for i in range(101,157):
    pro.append(i)

quan=[]
for i in range(50,150):
    quan.append(i)

values=[]
for i in range(0,200):
    order_id=order_id+1
    pid=(i%56)+101
    random_number_of_days = random.randrange(days_between_dates)
    order_date = start_date + datetime.timedelta(days=random_number_of_days)
    qu=random.choice(quan)
    temp=(pid,qu,order_date,'Pending')
    values.append(temp)
    print(values)

cu.executemany("INSERT into manager_order_list(product_id,quantity,order_date,order_status) values(?,?,?,?)",values)

cnxn.commit()    