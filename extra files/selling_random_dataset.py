# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:15:18 2020

@author: Jagseer Singh
"""

import random
import datetime   
import pyodbc
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

quan=[]
for i in range(5,25):
    quan.append(i)
quan2=[]
for i in range(60,100):
    quan2.append(i)
    

end_date=datetime.date.today()
start_date = end_date - datetime.timedelta(days=15)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

values=[]
for i in range(0,1000):
    random_number_of_days = random.randrange(days_between_dates)
    selling_date = start_date + datetime.timedelta(days=random_number_of_days)
    product_id=random.choice(pro)
    quantity=random.choice(quan)
    temp=(product_id,selling_date,quantity)
    values.append(temp)

for i in range(0,300):
    random_number_of_days = random.randrange(days_between_dates)
    selling_date = start_date + datetime.timedelta(days=random_number_of_days)
    product_id=random.choice(pro)
    quantity=random.choice(quan2)
    temp=(product_id,selling_date,quantity)
    values.append(temp)
    
    
    
cu.executemany("INSERT into selling_reports (product_id,selling_date,quantity) values(?,?,?)",values)
cnxn.commit()