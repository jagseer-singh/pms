# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 08:04:43 2020

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



al=[]
for i in range(0,26):
    temp=chr(65+i)
    al.append(temp)
    

lo=[]
for i in range(1,100):
    for j in al:
        i=str(i)
        temp=i+j
        lo.append(temp)

values=[]
cu.execute("select * from manager_order_list")
orders=cu.fetchall()

for i in range(0,150):
    sel=random.choice(orders)
    orders.remove(sel)
    start_date = sel[3]
    random_number_of_days = random.randrange(10)
    random_number_of_days = random_number_of_days+2
    rec_date = start_date + datetime.timedelta(days=random_number_of_days)
    
    
    random_number_of_days = random.randrange(300)
    random_number_of_days = random_number_of_days+2
    exp_date=start_date + datetime.timedelta(days=random_number_of_days)
    pid=sel[1]
    order_id=sel[0]
    qu=sel[2]
    loc=random.choice(lo)
    lo.remove(loc)
    if len(loc)==2:
        col=loc[0]
        she=loc[1]
    elif len(loc)==3:
        col=loc[0]
        col=col+loc[1]
        she=loc[2]
    tu=(pid,order_id,qu,exp_date,col,she)
    values.append(tu)
    
    
    cmd2=("update manager_order_list set order_status='Received',receiving_date=? where order_id=?")
    val2=(rec_date,order_id)
    cu.execute(cmd2,val2)
    
cu.executemany("INSERT into stock(product_id,order_id,quantity,expiry_date,columnno,shelfno) values(?,?,?,?,?,?)",values)

cnxn.commit()
        

        