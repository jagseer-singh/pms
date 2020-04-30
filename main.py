# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:27:11 2020

@author: Jagseer Singh
"""

from flask import Flask, render_template, request, flash, url_for, redirect, session
from passlib.hash import pbkdf2_sha256

from datetime import date
import datetime
import predicting_threshhold
import pyodbc

app=Flask(__name__)
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'
server = 'jagseer73.database.windows.net'
database = 'pharmacy'
username = 'root7'
password = 'cse@18103060'
driver= 'ODBC Driver 17 for SQL Server'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)




items=[]
predicting_threshhold.fnc()
today=date.today()
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])

def login():
    if (session.get('email')):
        session.pop('email', None)
        session.pop('type',None)
        session.pop('c_id',None)
    cur=cnxn.cursor()
    cmd=("delete from stock where expiry_date<=?")
    val=(today,)
    cur.execute(cmd,val)
    cnxn.commit()
    if request.method == 'POST':
        logininfo=request.form
        eemail=logininfo['email']
        password =logininfo['password']
        jobtype= logininfo['jobtype']
        if jobtype=="00":
            qr="SELECT passwd FROM managers where email = ?"
            e=(eemail,)
            cur.execute(qr,e)
            a=cur.fetchone()
            if(a == None):
                flash("You are not registered as a Manager, Please Contact Authority", 'danger')
                return redirect(url_for('login'))
            else:
                if (pbkdf2_sha256.verify(password,a[0])):
                    session['logged_in'] = True
                    session['email']=eemail
                    session['type']="00"
                    return redirect(url_for('dashboard_m'))
                else:
                    flash("WRONG PASSWORD", 'danger')
                    return redirect(url_for('login'))
        if jobtype=="11":
            qr="SELECT passwd FROM cocustomer where email = ?"
            e=(eemail,)
            cur.execute(qr,e)
            a=cur.fetchone()
            if(a == None):
                flash("You are not registered!!,REGISTER NOW", 'danger')
                return redirect(url_for('login'))
            else:
                if (pbkdf2_sha256.verify(password,a[0])):
                    cmd="SELECT c_id FROM cocustomer where email = ?"
                    val=(eemail,)
                    cur.execute(cmd,val)
                    cid=cur.fetchone()
                    session['logged_in'] = True
                    session['email']=eemail
                    session['type']="11"
                    session['c_id']=cid[0]
                    return redirect(url_for('profile_c'))
                else:
                    flash("WRONG PASSWORD", 'danger')
                    return redirect(url_for('login'))
        if jobtype=="22":
            qr="SELECT passwd FROM employees where email = ?"
            e=(eemail,)
            cur.execute(qr,e)
            a=cur.fetchone()
            if(a == None):
                flash("You are not registered!!,REGISTER NOW", 'danger')
                return redirect(url_for('login'))
            else:
                if (pbkdf2_sha256.verify(password,a[0])):
                    session['logged_in'] = True
                    session['email']=eemail
                    session['type']="22"
                    return redirect(url_for('profile_e'))
                else:
                    flash("WRONG PASSWORD", 'danger')
                    
                    return redirect(url_for('login'))
    
    return render_template('login.html',title='LOGIN')



@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        logininfo = request.form
        uname = logininfo['username']
        email = logininfo['email']
        mobile = logininfo['mobile']
        acc_type = logininfo['accounttype']
        password = logininfo['password']
        confirmpassword = logininfo['confirm_password']

        values = (uname, email, mobile, pbkdf2_sha256.hash(password))
        if acc_type== "11":
            if (password == confirmpassword):
                cur=cnxn.cursor()
                try:
                    cur.execute("INSERT into cocustomer(username,email,mobile,passwd) VALUES(?,?,?,?)",values)
                except:
                    flash("Account already exists",'info')
                    return redirect(url_for('signup'))
                else:
                    cnxn.commit()
                    cur.close()
                    flash("Thanks for Registering", 'success')
                    return redirect(url_for('login'))
            else:
                flash("Password did not match ", 'danger')
                return redirect(url_for('signup'))
        if acc_type== "22":
            if (password == confirmpassword):
                cur=cnxn.cursor()
                try:
                    cur.execute("INSERT into employees(username,email,mobile,passwd) VALUES(?,?,?,?)",values)
                except:
                    flash("Account already exists",'info')
                    return redirect(url_for('signup'))
                else:
                    cnxn.commit()
                    cur.close()
                    flash("Thanks for Registering", 'success')
                    return redirect(url_for('login'))
            else:
                flash("Password did not match ", 'danger')
                return redirect(url_for('signup'))

    return render_template('signup.html',title='Signup')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('type',None)
    session.pop('c_id',None)
    return redirect(url_for('login'))

@app.route('/dashboard_m')
def dashboard_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    today=date.today()
    temp=today+datetime.timedelta(days=7)
    cmd="select product_id,threshhold,stock_present from products where threshhold>stock_present"
    cur.execute(cmd)
    t=cur.fetchall()
    cmd="select product_id,expiry_date,columnno,shelfno from stock where ?<=expiry_date and ?>=expiry_date"
    val=(today,temp)
    cur.execute(cmd,val)
    e=cur.fetchall()
    return render_template('dashboard_m.html',table1=e,table2=t)


@app.route('/products_m')
def products_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    predicting_threshhold.fnc()
    cur=cnxn.cursor()
    cmd="select * from products"
    cur.execute(cmd)
    p=cur.fetchall()
    return render_template('products_m.html',table=p)



@app.route('/stock_m',methods=["GET","POST"])
def stock_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""Select stock.product_id,products.company_name,products.product_name, stock.quantity, stock.expiry_date, stock.columnno, stock.shelfno 
                from stock INNER JOIN products ON stock.product_id=products.product_id
                """)
    st=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="bt1":
            product_id=info['productid']
            cmd=("""Select stock.product_id,products.company_name,products.product_name, stock.quantity, stock.expiry_date, stock.columnno, stock.shelfno 
                from stock INNER JOIN products ON stock.product_id=products.product_id and products.product_id=?""")
            val=(product_id,)
            cur.execute(cmd,val)
            st=cur.fetchall()
        elif info['bt']=="bt2":
            expdate_before=info['expirydate']
            cmd=("""Select stock.product_id,products.company_name,products.product_name, stock.quantity, stock.expiry_date, stock.columnno, stock.shelfno 
                from stock INNER JOIN products ON stock.product_id=products.product_id and stock.expiry_date<=?""")
            val=(expdate_before,)
            cur.execute(cmd,val)
            st=cur.fetchall()
            
    return render_template('stock_m.html',table=st)

@app.route('/place_order_m',methods=['GET','POST'])
def place_order_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    if request.method=="POST":
        info=request.form
        productID=info['productID']
        quantity=info['quantity']
        if(int(quantity)<=0):
            flash("Enter valid quantity", 'danger')
            return redirect(url_for('place_order_m'))
        cur=cnxn.cursor()
        cmd="SELECT * from products where product_id=?"
        val=(productID,)
        cur.execute(cmd,val)
        productOrdered=cur.fetchone()
        if productOrdered==None:
            flash("Enter valid PRODUCT ID", 'danger')
            return redirect(url_for('place_order_m'))
        else:
            return redirect(url_for('confirmation_m',pid=productID,quantity=quantity))

    return render_template('place_order_m.html')
	

@app.route('/confirmation_m',methods=["GET","POST"])
def confirmation_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    productID=request.args['pid']
    quantity=request.args['quantity']
    cur=cnxn.cursor()
    cmd=("Select product_name,company_name,price from products where product_id=?")
    val=(productID,)
    cur.execute(cmd,val)
    a=cur.fetchone()
    amount=int(a[2])*int(quantity)
    details=(productID,a[0],a[1],quantity,date.today(),amount)
    if request.method=="POST":
        info=request.form
        if info['bt']=="cancel":
            flash("Cancelled",'success')
            return redirect(url_for('place_order_m'))
        elif info['bt']=="place":
            values=(productID,quantity,date.today(),"Pending")
            cur.execute("INSERT into manager_order_list(product_id,quantity,order_date,order_status) VALUES(?,?,?,?)",values)
            cnxn.commit()
            cur.close()
            flash("ORDER SUCCESSFUL", 'success')
            return redirect(url_for('place_order_m'))
            
    return render_template('confirmation_m.html',info=details)

@app.route('/order_list_m',methods=['GET','POST'])
def order_list_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id order by manager_order_list.order_date desc""")
    orders=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            p_id=info['pid']
            cmd="""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and manager_order_list.product_id=?"""
            vl=(p_id,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button2":
            ord_date=info['orderdate']
            cmd="""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_date=?"""
            vl=(ord_date,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button3":
            ord_st=info['orderstatus']
            if ord_st == "12":
                cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_status='Pending'""")
                orders=cur.fetchall()
            elif ord_st=="13":
                cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_status='Received'""")
                orders=cur.fetchall()
            
    return render_template('order_list_m.html',table=orders)

@app.route('/profile_m')
def profile_m():
    try:
        email=session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    qr="SELECT * FROM managers where email = ?"
    e=(email,)
    cur.execute(qr,e)
    a=cur.fetchone()
    return render_template('profile_m.html',info=a)

@app.route('/selling_reports_m',methods=["GET","POST"])
def selling_reports_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""Select selling_reports.product_id,products.product_name,products.company_name,selling_reports.quantity,selling_reports.selling_date
                 from selling_reports INNER JOIN products ON products.product_id=selling_reports.product_id order by selling_reports.selling_date desc""")
    reports=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            pid=info['pid']
            cmd="""Select selling_reports.product_id,products.product_name,products.company_name,selling_reports.quantity,selling_reports.selling_date
                 from selling_reports INNER JOIN products ON products.product_id=selling_reports.product_id  where selling_reports.product_id=? order by selling_reports.selling_date desc"""
            vl=(pid,)
            cur.execute(cmd,vl)
            reports=cur.fetchall()
        elif info['bt']=="button2":
            selling_date=info['sellingdate']
            cmd="""Select selling_reports.product_id,products.product_name,products.company_name,selling_reports.quantity,selling_reports.selling_date
                 from selling_reports INNER JOIN products ON products.product_id=selling_reports.product_id where selling_reports.selling_date=?
                 order by selling_reports.selling_date desc"""
            vl=(selling_date,)
            cur.execute(cmd,vl)
            reports=cur.fetchall()
        elif info['bt']=="button3":
            tp=info['timeperiod']
            
            if tp == "12":
                date=today - datetime.timedelta(days=3)
                cmd=("""Select selling_reports.product_id,products.product_name,products.company_name,selling_reports.quantity,selling_reports.selling_date
                 from selling_reports INNER JOIN products ON products.product_id=selling_reports.product_id 
                  where selling_reports.selling_date >=? order by selling_reports.product_id""")
                val=(date,)
                cur.execute(cmd,val)
                reports=cur.fetchall()
            elif tp=="13":
                date=today - datetime.timedelta(days=7)
                cmd=("""Select selling_reports.product_id,products.product_name,products.company_name,selling_reports.quantity,selling_reports.selling_date
                 from selling_reports INNER JOIN products ON products.product_id=selling_reports.product_id 
                  where selling_reports.selling_date >=? order by selling_reports.product_id""")
                val=(date,)
                cur.execute(cmd,val)
                reports=cur.fetchall()
    return render_template('selling_reports_m.html',table=reports)

@app.route('/corporate_order_m',methods=["GET","POST"])
def corporate_order_m():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "00":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id""")
    
    orders=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            ord_id=info['orderno']
            cmd="""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_id=?"""
            vl=(ord_id,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button2":
            ord_date=info['orderdate']
            cmd="""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_date=?"""
            vl=(ord_date,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button3":
            ord_st=info['orderstatus']
            if ord_st == "12":
                cur.execute("""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Pending'""")
                orders=cur.fetchall()
            elif ord_st=="13":
                cur.execute("""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Received' """)
                orders=cur.fetchall()
                
    return render_template('corporate_order_m.html',table=orders)
    
    

@app.route('/profile_e')
def profile_e():
    try:
        email=session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    qr="SELECT * FROM employees where email =?"
    e=(email,)
    cur.execute(qr,e)
    a=cur.fetchone()
    today=date.today()
    temp=today+datetime.timedelta(days=7)
    cmd="select product_id,expiry_date,columnno,shelfno from stock where ?<=expiry_date and ?>=expiry_date"
    val=(today,temp,)
    cur.execute(cmd,val)
    e=cur.fetchall()
    return render_template('profile_e.html',info=a,table=e)

@app.route('/received_e',methods=["GET","POST"])
def received_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    if request.method=="POST":
        info=request.form
        order_id=info['orderid']
        quantity=info['quantity']
        expiry=info['expirydate']
        columnno=info['columnno']
        shelf=info['shelfno']
        cur=cnxn.cursor()
        cmd1=("Select * from stock where columnno=? and shelfno=?")
        val1=(columnno,shelf)
        cur.execute(cmd1,val1)
        temp=cur.fetchone()
        if temp==None:
            cmd=("Select * from manager_order_list where order_id=?")
            val=(order_id,)
            cur.execute(cmd,val)
            a=cur.fetchone()
            if a==None:
                flash("Enter valid Order ID", 'danger')
                return redirect(url_for('received_e'))
            else:
                if int(quantity) != a[2]:
                    flash("Entered quantity doesn't match ordered quantity, Contact Manager", 'danger')
                    return redirect(url_for('received_e'))
                else:
                    if a[4]=="Pending":
                        format_str = '%Y-%m-%d'
                        expiry_d = datetime.datetime.strptime(expiry, format_str).date()
                        if  expiry_d >= date.today():
                            cmd2=("update manager_order_list set order_status='Received' ,receiving_date=? where order_id=?")
                            val2=(date.today(),order_id)
                            cur.execute(cmd2,val2)
                            values=(a[1],order_id,quantity,expiry,columnno,shelf)
                            cur.execute("INSERT into stock (product_id, order_id ,quantity,expiry_date,columnno,shelfno) values(?,?,?,?,?,?)",values)
                            cnxn.commit()
                            flash("SUCCESSFUL", 'success')
                            return redirect(url_for('received_e'))
                        else:
                            flash("Product is already expired, Contact seller",'danger')
                    else:
                        flash("This order is already received, Please Check",'danger')
                        return redirect(url_for('received_e'))
        else:
            flash("This shelf and column is already occupied",'danger')
            return redirect(url_for('received_e'))
                
        
    return render_template('received_e.html')

@app.route('/selling_e',methods=["GET","POST"])
def selling_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    if request.method=="POST":
        info=request.form
        if info['bt']=="addmore":
            p_id=info['p_id']
            quantity=info['quantity']
            quantity=int(quantity)
            for i in items:
                if i[0]==p_id:
                    quantity=i[1]+quantity
            cmd=("Select quantity from stock where product_id=?")
            val=(p_id,)
            cur.execute(cmd,val)
            q=cur.fetchall()
            q_present=0
            for i in q:
                q_present=q_present+i[0]
                
            if q_present>=quantity:    
                temp=[p_id,quantity]
                for i in items:
                    if i[0]==p_id:
                        items.remove(i)
                items.append(temp)
                flash("SUCCESSFUL",'success')
                return redirect(url_for('selling_e'))
            else:
                flash("NOT ENOUGH ITEMS IN STOCK",'danger')
                return redirect(url_for('selling_e'))
        elif info['bt']=="producebill":
            if len(items)==0:
                flash("Nothing in the list",'danger')
                return redirect(url_for('selling_e'))
            else:
                return redirect(url_for('bill_e'))
        elif info['bt']=="discard":
            items.clear()
            flash("Everything Discarded",'success')
            return redirect(url_for('selling_e'))
    return render_template('selling_e.html')


@app.route('/bill_e',methods=["GET","POST"])
def bill_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    bill_list=[]
    total_amount=0
    for i in items:
        p_id=i[0]
        quantity=i[1]
        cmd="""Select products.product_id,products.product_name,products.company_name,products.price,stock.order_id,stock.quantity,stock.columnno,
        stock.shelfno from stock INNER JOIN products ON products.product_id=stock.product_id where stock.product_id=? order by stock.expiry_date"""
        val=(p_id,)
        cur.execute(cmd,val)
        w=cur.fetchall()
        temp_q=quantity
        for j in w:
            if j[5]>=temp_q:
                product_id=j[0]
                product_name=j[1]
                company_name=j[2]
                amount=temp_q*j[3]
                total_amount=total_amount+amount
                order_id=j[4]
                quan=temp_q
                col=j[6]
                she=j[7]
                l=(product_id,product_name,company_name,amount,order_id,quan,col,she)
                bill_list.append(l)
                temp_q=0
                break
            else:
                temp_q=temp_q-j[5]
                product_id=j[0]
                product_name=j[1]
                company_name=j[2]
                amount=j[5]*j[3]
                total_amount=total_amount+amount
                order_id=j[4]
                quan=j[5]
                col=j[6]
                she=j[7]
                l=(product_id,product_name,company_name,amount,order_id,quan,col,she)
                bill_list.append(l)
                
    if request.method=="POST":
        info=request.form
        if info['bt']=="bill":
            
            for i in bill_list:
                productid_sold=i[0]
                orderid_sold=i[4]
                quantity_sold=i[5]
                cmd1="Select quantity from stock where order_id=?"
                val1=(orderid_sold,)
                cur.execute(cmd1,val1)
                temp=cur.fetchone()
                if temp[0]==quantity_sold:
                    cmd2="INSERT into selling_reports (product_id,quantity,selling_date) values(?,?,?)"
                    val2=(productid_sold,quantity_sold,date.today())
                    cur.execute(cmd2,val2)
                    cnxn.commit()
                    cmd3="Delete from stock where order_id=?"
                    val3=(orderid_sold,)
                    cur.execute(cmd3,val3)
                    cnxn.commit()
                    #clear stock
                elif temp[0] > quantity_sold:
                    cmd2="INSERT into selling_reports (product_id,quantity,selling_date) values(?,?,?)"
                    val2=(productid_sold,quantity_sold,date.today())
                    cur.execute(cmd2,val2)
                    cnxn.commit()
                    cmd3="update stock set quantity=? where order_id=?"
                    rem=temp[0]-quantity_sold
                    val3=(rem,orderid_sold)
                    cur.execute(cmd3,val3)
                    cnxn.commit()
                    #decrease stock
            items.clear()
            flash('BILL GENERATED','success')    
            return redirect(url_for('selling_e'))
        elif info['bt']=="add":
            flash("ADD MORE",'success')
            return redirect(url_for('selling_e'))
        elif info['bt']=="discard":
            flash("DISCARDED",'success')
            items.clear()
            return redirect(url_for('selling_e'))
    return render_template('bill_e.html',table=bill_list,t_amount=total_amount)


@app.route('/order_list_e',methods=["GET","POST"])
def order_list_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id""")
    orders=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            ord_no=info['orderno']
            cmd="""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_id=?"""
            vl=(ord_no,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button2":
            ord_date=info['orderdate']
            cmd="""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_date=?"""
            vl=(ord_date,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button3":
            ord_st=info['orderstatus']
            if ord_st == "12":
                cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_status='Pending'""")
                orders=cur.fetchall()
            elif ord_st=="13":
                cur.execute("""SELECT manager_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   manager_order_list.quantity, manager_order_list.order_date,manager_order_list.order_status 
                   FROM manager_order_list
                   INNER JOIN products ON manager_order_list.product_id=products.product_id and order_status='Received'""")
                orders=cur.fetchall()
            
    return render_template('order_list_e.html',table=orders)



@app.route('/co_order_list_e',methods=["GET","POST"])
def co_order_list_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cur.execute("""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id""")
    
    orders=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            ord_id=info['orderno']
            cmd="""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_id=?"""
            vl=(ord_id,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button2":
            ord_date=info['orderdate']
            cmd="""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_date=?"""
            vl=(ord_date,)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button3":
            ord_st=info['orderstatus']
            if ord_st == "12":
                cur.execute("""SELECT cocustomer_order_list.c_id,cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Pending'""")
                orders=cur.fetchall()
            elif ord_st=="13":
                cur.execute("""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Received' """)
                orders=cur.fetchall()
         
    return render_template('co_order_list_e.html',table=orders)
    


@app.route('/co_selling_e',methods=["GET","POST"])
def co_selling_e():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    if request.method=="POST":
        info=request.form
        order_id=info['order_id']
        c_id=info['c_id']
        c_id=int(c_id)
        cmd=("""SELECT cocustomer_order_list.order_id,cocustomer_order_list.c_id,products.product_id, products.company_name, products.product_name,
                       cocustomer_order_list.quantity,cocustomer_order_list.order_status 
                       FROM cocustomer_order_list
                       INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and cocustomer_order_list.order_id=?""")
        val=(order_id,)
        cur.execute(cmd,val)
        order=cur.fetchone()
        if order==None:
            flash("No Such Order",'danger')
            return redirect(url_for('co_selling_e'))
        else:
            if c_id==order[1]:
                if order[6] != 'Pending':
                    flash("Order already sent, Status is not pending",'danger')
                    return redirect(url_for('co_selling_e'))
                else:
                    p_id=order[2]
                    cmd=("Select quantity from stock where product_id=?")
                    val=(p_id,)
                    cur.execute(cmd,val)
                    q=cur.fetchall()
                    q_present=0
                    for i in q:
                        q_present=q_present+i[0]
                    if q_present>=order[5]:
                        """cmd=("update cocustomer_order_list set order_status='Sent' where order_id=?")
                        val=(order[0],)
                        cur.execute(cmd,val)
                        cnxn.commit()
                        flash("SUCCESS!!!",'success')"""
                        return redirect(url_for('bill_c',order_id=order[0],c_id=order[1],p_id=order[2],quantity=order[5]))
                    else:
                        flash("Not enough Stock present",'danger')
                        return redirect(url_for('co_selling_e'))        
            else:
                flash("Customer ID do not match",'danger')
                return redirect(url_for('co_selling_e'))
                
                
    return render_template('co_selling_e.html')

@app.route('/bill_c',methods=["GET","POST"])
def bill_c():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "22":
        return redirect(url_for('login'))
    co_order_id=request.args['order_id']
    c_id=request.args['c_id']
    p_id=request.args['p_id']
    quantity=request.args['quantity']
    quantity=int(quantity)
    cur=cnxn.cursor()
    bill_list=[]
    total_amount=0
    cmd="""Select products.product_id,products.product_name,products.company_name,products.price,stock.order_id,stock.quantity,stock.columnno,
    stock.shelfno from stock INNER JOIN products ON products.product_id=stock.product_id where stock.product_id=? order by stock.expiry_date"""
    val=(p_id,)
    cur.execute(cmd,val)
    w=cur.fetchall()
    price=w[0][3]
    p_name=w[0][1]
    com_name=w[0][2]
    total_amount=price*quantity
    details=[c_id,p_id,p_name,com_name,quantity,total_amount]
    temp_q=quantity
    for j in w:
        if j[5]>=temp_q:
            amount=temp_q*j[3]
            order_id=j[4]
            quan=temp_q
            col=j[6]
            she=j[7]
            l=(quan,col,she,amount,order_id)
            bill_list.append(l)
            temp_q=0
            break
        else:
            temp_q=temp_q-j[5]
            amount=j[5]*j[3]
            order_id=j[4]
            quan=j[5]
            col=j[6]
            she=j[7]
            l=(quan,col,she,amount,order_id)
            bill_list.append(l)
    
    if request.method=="POST":
        productid_sold=p_id
        cmd=("update cocustomer_order_list set order_status='Sent' where order_id=?")
        val=(co_order_id,)
        cur.execute(cmd,val)
        cnxn.commit()
        for i in bill_list:
                orderid_sold=i[4]
                quantity_sold=i[0]
                cmd1="Select quantity from stock where order_id=?"
                val1=(orderid_sold,)
                cur.execute(cmd1,val1)
                temp=cur.fetchone()
                if temp[0]==quantity_sold:
                    cmd2="INSERT into selling_reports (product_id,quantity,selling_date) values(?,?,?)"
                    val2=(productid_sold,quantity_sold,date.today())
                    cur.execute(cmd2,val2)
                    cnxn.commit()
                    cmd3="Delete from stock where order_id=?"
                    val3=(orderid_sold,)
                    cur.execute(cmd3,val3)
                    cnxn.commit()
                    #clear stock
                elif temp[0] > quantity_sold:
                    cmd2="INSERT into selling_reports (product_id,quantity,selling_date) values(?,?,?)"
                    val2=(productid_sold,quantity_sold,date.today())
                    cur.execute(cmd2,val2)
                    cnxn.commit()
                    cmd3="update stock set quantity=? where order_id=?"
                    rem=temp[0]-quantity_sold
                    val3=(rem,orderid_sold)
                    cur.execute(cmd3,val3)
                    cnxn.commit()
                    #decrease stock
        flash('ORDER SENT SUCCESSFULLY!!!','success')
        return redirect(url_for('co_selling_e'))
        
    return render_template('bill_c.html',info=details,table=bill_list)    
    
@app.route('/profile_c')
def profile_c():
    try:
        email=session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "11":
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cmd=("Select * from cocustomer where email=?")
    val=(email,)
    cur.execute(cmd,val)
    a=cur.fetchone()
    return render_template('profile_c.html',data=a)


@app.route('/place_order_c',methods=["GET","POST"])
def place_order_c():
    try:
        c_id=session['c_id']
    except:
        return redirect(url_for('login'))
    if request.method=="POST":
        info=request.form
        p_id=info['productid']
        quantity=info['quantity']
        quantity=int(quantity)
        if(quantity<=0):
            flash("Enter valid quantity", 'danger')
            return redirect(url_for('place_order_c'))
        cur=cnxn.cursor()
        cmd="SELECT * from products where product_id=?"
        val=(p_id,)
        cur.execute(cmd,val)
        productOrdered=cur.fetchone()
        if productOrdered==None:
            flash("Enter valid PRODUCT ID", 'danger')
            return redirect(url_for('place_order_c'))
        else:
            return redirect(url_for('confirmation_c',pid=p_id,cid=c_id,quantity=quantity))
    return render_template('place_order_c.html')

@app.route('/confirmation_c',methods=["GET","POST"])
def confirmation_c():
    try:
        session['email']
    except:
        return redirect(url_for('login'))
    if session['type'] != "11":
        return redirect(url_for('login'))
    c_id=request.args['cid']
    p_id=request.args['pid']
    quantity=request.args['quantity']
    cur=cnxn.cursor()
    cmd=("Select product_name,company_name,price from products where product_id=?")
    val=(p_id,)
    cur.execute(cmd,val)
    a=cur.fetchone()
    amount=int(a[2])*int(quantity)
    details=(p_id,a[0],a[1],quantity,date.today(),amount)
    if request.method=="POST":
        info=request.form
        if info['bt']=="cancel":
            flash("Cancelled",'success')
            return redirect(url_for('place_order_c'))
        elif info['bt']=="place":
            values=(c_id,p_id,quantity,date.today(),"Pending")
            cur.execute("INSERT into cocustomer_order_list(c_id,product_id,quantity,order_date,order_status) VALUES(?,?,?,?,?)",values)
            cnxn.commit()
            cur.close()
            flash("ORDER SUCCESSFUL", 'success')
            return redirect(url_for('place_order_c'))
            
    return render_template('confirmation_c.html',info=details)

@app.route('/co_order_list_c',methods=["GET","POST"])
def co_order_list_c():
    try:
        c_id=session['c_id']
    except:
        return redirect(url_for('login'))
    cur=cnxn.cursor()
    cmd=("""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and c_id=?""")
    val=(c_id,)
    cur.execute(cmd,val)
    orders=cur.fetchall()
    if request.method=="POST":
        info=request.form
        if info['bt']=="button1":
            ord_id=info['orderno']
            cmd="""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_id=? and c_id=?"""
            vl=(ord_id,c_id)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button2":
            ord_date=info['orderdate']
            cmd="""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_date=? and c_id=?"""
            vl=(ord_date,c_id)
            cur.execute(cmd,vl)
            orders=cur.fetchall()
        elif info['bt']=="button3":
            ord_st=info['orderstatus']
            if ord_st == "12":
                cmd=("""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Pending' and c_id=?""")
                val=(c_id,)
                cur.execute(cmd,val)
                orders=cur.fetchall()
            elif ord_st=="13":
                cmd=("""SELECT cocustomer_order_list.order_id,products.product_id, products.company_name, products.product_name,
                   cocustomer_order_list.quantity, cocustomer_order_list.order_date,cocustomer_order_list.order_status 
                   FROM cocustomer_order_list
                   INNER JOIN products ON cocustomer_order_list.product_id=products.product_id and order_status='Received' and c_id=?""")
                val=(c_id,)
                cur.execute(cmd,val)
                orders=cur.fetchall()
	for i in orders:
	    if i[6]=='Sent':
			i[6]='Received'
    return render_template('co_order_list_c.html',table=orders)
    
if __name__ == '__main__':
    app.run()
    
    
    
