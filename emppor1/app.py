from flask import Flask,render_template,flash,redirect,request,url_for,session,logging,abort
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt
# from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
import os
from functools import wraps
app=Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# app.config['SECRET_KEY']='Thisissupposedtobesecret!'
gmail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shivam.vku@gmail.com'
app.config['MAIL_PASSWORD'] = '7569880950vineet'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
gmail = Mail(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskappemp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)#https://realpython.com/blog/python/the-minimum-viable-test-suite/

@app.route('/')
def home():
	return render_template('home.html')
@app.route('/home111')
def home111():
  return render_template('home1.html')
#---------------------------------nextregi-----------------------
class Councling(Form):
  name = StringField('name', [validators.Length(min =2 , max = 20)])
  date_of_brith = StringField('date_of_brith', [validators.Length(min =2 , max = 20)])
  father_mother_name = StringField('father_mother_name', [validators.Length(min =2 , max = 20)]) 
@app.route('/councling', methods = ['GET', 'POST'])

def councling():
   form = Councling(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello') 
       name = form.name.data
       date_of_brith = form.date_of_brith.data
       father_mother_name = form.father_mother_name.data
       cur=mysql.connection.cursor()
       cur.execute('''SELECT * FROM employees WHERE Name =%s AND Date_Brith=%s AND Father_Mother_Name=%s''',(name,date_of_brith,father_mother_name))
       rv=cur.fetchall()

       return render_template('council1.html',rv=rv)
   return render_template('council.html',form = form)

#-----------------------------------------------------------------
@app.route('/12')
def home12():
  return render_template('upload.html')

#--------------------------uploads--------------------
@app.route("/upload", methods=["GET","POST"])
def upload():
  target=os.path.join(APP_ROOT,'images/')
  print (target)

  if not os.path.isdir(target):
    os.mkdir(target)
  for file in request.files.getlist("file"):
    print (file)
    filename = file.filename
    destination = "/".join([target, filename])
    print (destination)
    file.save(destination)
  print("hello")
  return redirect(url_for())

#----------------------------leave------------------
class Leaves(Form):
 empid = StringField('Employee Id',[validators.Length(min=1,max=50)])
 empname = StringField('Employee Name',[validators.Length(min=1,max=50)])
 department = SelectField(u'Department', choices=[('None','None'),('UI','UI'),('Python','Python'),('Marketing','Marketing')])
 leavefrom = DateField('Leave From', format='%Y-%m-%d')
 leaveto = DateField('Leave To', format='%Y-%m-%d')
 Number_of_days = StringField('Number_of_days',[validators.Length(min=1,max=2)])
 Reason = TextAreaField('Reason',[validators.Length(min=1,max=50)])
 

@app.route('/leaves', methods = ['GET', 'POST'])

def leaves():
  form = Leaves(request.form)
  if request.method == 'POST' and form.validate():
      empid=form.empid.data
      empname = form.empname.data
      department = form.department.data
      leavefrom = form.leavefrom.data
      leaveto = form.leaveto.data
      Number_of_days = form.Number_of_days.data
      Reason = form.Reason.data
      status = 'null'
      cur=mysql.connection.cursor()
      cur.execute("INSERT INTO leaves(emp_id,emp_name,department,leave_form,leave_to,Number_of_days,reason,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(empid,empname,department,leavefrom,leaveto,Number_of_days,Reason,status))
      mysql.connection.commit()
      cur.execute("SELECT * FROM leaves")
      rv=cur.fetchall()
      rv1=list(rv)
      rv=rv1[0]
      print(rv)
      return render_template('leavestatus.html',rv1=rv1)     
  return render_template('leave.html',form = form)

#------------------------------empleavestatus---------------
@app.route('/empleavestatus')
def empleavestatus():
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM leaves ")
  rv=cur.fetchall()
  rv1=list(rv)
  print(rv1)
  return render_template('leavestatus.html',rv1=rv1)
  

#------------------------------adminApprivel---------------
@app.route('/adminapporal')
def adminapporal():
  name='null'
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM leaves WHERE status ='"+name+"'")
  rv=cur.fetchall()  
  print(rv)
  return render_template('leave1.html',rv=rv)
  

#--------------------------------Approvel--------------------------
@app.route('/Approvel')
def Approvel():
  eid=request.args.get('id')
  cur=mysql.connection.cursor()
  cur.execute("UPDATE `leaves` SET `status`='Approvel' WHERE emp_id=%s",[eid])
  mysql.connection.commit()
  cur.execute("SELECT * FROM leaves WHERE status ='"+name+"'")
  rv=cur.fetchall()
  return render_template('leave1.html',rv=rv)
#--------------------------------Cancel--------------------------
@app.route('/cancel')
def cancel():
  eid=request.args.get('id')
  cur=mysql.connection.cursor()
  cur.execute("UPDATE `leaves` SET `status`='Not-Approvel' WHERE emp_id=%s",[eid])
  mysql.connection.commit()
  cur.execute("SELECT * FROM leaves WHERE status ='"+name+"'")
  rv=cur.fetchall()
  return render_template('leave1.html',rv=rv)
#---------------------------back-------------------------------
@app.route('/back')
def back():
  eid=request.args.get('id')
  cur=mysql.connection.cursor()
  cur.execute("UPDATE `leaves` SET `status`='Approvel' WHERE emp_id=%s",[eid])
  rv=cur.fetchall()
  print(rv)
  return render_template('update.html',person=person)
#--------------------next--------------------------------
@app.route('/next')
def next():
  id=request.args.get('id')
  
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id=%s",[id])
  rv=cur.fetchall()
  person=rv[0]
  print(person['Type'])
  if(person['Type']=="FULLTIME"):
    print("fullif")
    return render_template('fulltime1.html',person=person)
  elif(person['Type']=="PARTTIME"):
    print("partif")
    return render_template('parttime1.html',person=person)
  else:
    return render_template('intends1.html',person=person)

#------------------------EMPDETAILES--------------------------------
@app.route('/empdetails')
def empdetails():
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM full_emps")
  rv=cur.fetchall()
  person=list(rv)
  
  print(person[0]['id'])
  return render_template('employeedetails.html',person=person)

#------------------------payslip--------------------------------
class Payslip(Form):
  name = StringField('name', [validators.Length(min =2 , max = 20)])
  date_of_brith = StringField('date_of_brith', [validators.Length(min =2 , max = 20)])
  Phone_num = StringField('Phone_num', [validators.Length(min =2 , max = 20)]) 
@app.route('/payslip', methods = ['GET', 'POST'])

def payslip():
   form = Payslip(request.form)
   print('hiii')
   if request.method == 'POST' and form.validate():
       print('hello')
       name = form.name.data
       date_of_brith = form.date_of_brith.data
       Phone_num = form.Phone_num.data
       cur=mysql.connection.cursor()
       cur.execute('''SELECT * FROM employees WHERE Name =%s AND Date_Brith=%s AND Phone_number=%s''',(name,date_of_brith,Phone_num))
       rv1=cur.fetchall()
       rv=list(rv1)
       rv=rv[0]
       print(rv)
       cur.execute("SELECT * FROM payments WHERE Name = '"+name+"'")
       person1=cur.fetchall()
       person=list(person1)
       person=person[0]
       print(person)
       return render_template('payslip1.html',rv=rv,person=person)
   return render_template('payslip.html',form = form)

#------------------------payments--------------------------------
class Payments(Form):
  empid = StringField('Empid', [validators.Length(min =1 , max = 20)])
  name = StringField('Name', [validators.Length(min =2 , max = 20)])
  department = StringField('Department', [validators.Length(min =2 , max = 20)])
  mounth = StringField('Mounth', [validators.Length(min =2 , max = 20)])
  leavedays = StringField('Leave Days', [validators.Length(min =1 , max = 20)])
  actualctc = StringField('Actual CTC', [validators.Length(min =2 , max = 20)])
  payblectc = StringField('Payble CTC', [validators.Length(min =2 , max = 20)])
   
@app.route('/payments', methods = ['GET', 'POST'])

def payment():
   form = Payments(request.form)
   if request.method == 'POST' and form.validate():
       print('hello')
       empid = form.empid.data
       name = form.name.data
       department = form.department.data
       mounth = form.mounth.data
       leavedays = form.leavedays.data
       actualctc = form.actualctc.data
       payblectc = form.payblectc.data
       print("mounth::",mounth)
       cur=mysql.connection.cursor()
       cur.execute("INSERT INTO `payments`(`emp_id`, `name`, `department`, `mounth`, `leave_days`, `actual_ctc`, `payble_ctc`) VALUES(%s,%s,%s,%s,%s,%s,%s)",(empid,name,department,mounth,leavedays,actualctc,payblectc))
       mysql.connection.commit()

       return render_template('home.html')
   return render_template('payment.html',form = form)
#-------------------------------fulltime1------------
@app.route('/fulltime1')

def fulltime1(): 
  id1=request.args.get('idel')

  Date_Of_Joining=request.args.get('DOB')
  Department=request.args.get('Department')
  sel=request.args.get('sel')
  Payrole=request.args.get('Payrole')
  Remarks=request.args.get('Remarks')
 

  
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id='"+id1+"'")
  rv=cur.fetchall()
  a=list(rv)
  p1=a[0]['Name']
  p2=a[0]['Date_Brith']
  p3=a[0]['Address']
  # p4=a[0]['Aadhar_number']
  p5=a[0]['Phone_number']
  p6=a[0]['Email_id']
  p7=a[0]['Alternate_no']
  p8=a[0]['Type']
  

  print("in full fun")
  cur = mysql.connection.cursor()

  cur.execute("INSERT INTO full_emps(Name,Date_Brith,Address,Phone_num,Email,Alternate_num,Type,Date_join,Post,Pay_role,Dep,Remark) VALUES('"+p1+"','"+p2+"','"+p3+"','"+p5+"','"+p6+"','"+p7+"','"+p8+"','"+Date_Of_Joining+"','"+sel+"','"+Payrole+"','"+Department+"','"+Remarks+"')")

  mysql.connection.commit()
  
  return redirect(url_for('signup'))

#--------------------------------------------------------
@app.route('/parttime1')

def parttime1(): 
  id1=request.args.get('idel')

  Date_Of_Joining=request.args.get('DOB')
  Department=request.args.get('Department')
  sel=request.args.get('sel')
  Payrole=request.args.get('Payrole')
  Remarks=request.args.get('Remarks')
  print("in part fun")

  
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id='"+id1+"'")
  rv=cur.fetchall()
  a=list(rv)
  p1=a[0]['Name']
  p2=a[0]['Date_Brith']
  p3=a[0]['Address']
  # p4=a[0]['Aadhar_number']
  p5=a[0]['Phone_number']
  p6=a[0]['Email_id']
  p7=a[0]['Alternate_no']
  p8=a[0]['Type']
  

  print(p2)
  cur = mysql.connection.cursor()

  cur.execute("INSERT INTO part_emps(Name,Date_Brith,Address,Phone_num,Email,Alternate_num,Type,Date_join,Post,Pay_role,Dep,Remark) VALUES('"+p1+"','"+p2+"','"+p3+"','"+p5+"','"+p6+"','"+p7+"','"+p8+"','"+Date_Of_Joining+"','"+sel+"','"+Payrole+"','"+Department+"','"+Remarks+"')")

  mysql.connection.commit()
  
  return redirect(url_for('signup'))

#--------------------------------------------------------
@app.route('/intens1')

def intens1(): 
  id1=request.args.get('idel')

  Date_Of_Joining=request.args.get('DOB')
  Department=request.args.get('Department')
  sel=request.args.get('sel')
  Payrole=request.args.get('Payrole')
  Remarks=request.args.get('Remarks')
 

  
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id='"+id1+"'")
  rv=cur.fetchall()
  a=list(rv)
  p1=a[0]['Name']
  p2=a[0]['Date_Brith']
  p3=a[0]['Address']
  # p4=a[0]['Aadhar_number']
  p5=a[0]['Phone_number']
  p6=a[0]['Email_id']
  p7=a[0]['Alternate_no']
  p8=a[0]['Type']
  

  print(p2)
  cur = mysql.connection.cursor()

  cur.execute("INSERT INTO intend_emps(Name,Date_Brith,Address,Phone_num,Email,Alternate_num,Type,Date_join,Post,Pay_role,Dep,Remark) VALUES('"+p1+"','"+p2+"','"+p3+"','"+p5+"','"+p6+"','"+p7+"','"+p8+"','"+Date_Of_Joining+"','"+sel+"','"+Payrole+"','"+Department+"','"+Remarks+"')")

  mysql.connection.commit()
  
  return redirect(url_for('signup'))

#--------------------------------------------------------
@app.route('/back12')

def back12(): 
  name=request.args.get('name')
  father_mother_name=request.args.get('father_mother_name')
  date_of_brith=request.args.get('date_of_brith')
  address=request.args.get('address')
  mobile=request.args.get('mobile')
  email=request.args.get('email')
  alternate_no=request.args.get('alternate_no')
  type1=request.args.get('type')
  aadhar_number=request.args.get('aadhar_number')
  id1=request.args.get('idel')
  print(id1)
  
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id='"+id1+"'")
  rv=cur.fetchall()
  a=list(rv)
  print("rvv",list(rv))
  
  c=a[0]['id']

  cur=mysql.connection.cursor()
  cur.execute("UPDATE `employees` SET `Name`=%s,`Father_Mother_Name`=%s,`Date_Brith`=%s,`Address`=%s,`Aadhar_number`=%s,`Phone_number`=%s,`Email_id`=%s,`Alternate_no`=%s,`Type`=%s WHERE id=%s",[name,father_mother_name,date_of_brith,address,aadhar_number,mobile,email,alternate_no,type1,c])
  rv1=cur.fetchall()
  print(rv1)
  mysql.connection.commit()

  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM employees WHERE id='"+id1+"'")
  rv2=cur.fetchall()
  print("rv2",rv2)

  return redirect(url_for('home'))
#----------------------------------emppages----------------
     
#----------------------------------------------------------

@app.route('/home')
def index():
	cur=mysql.connection.cursor()
	cur.execute('''SELECT * FROM examle''')
	rv=cur.fetchall()
	# return str(rv)

	return render_template('index.html',rv=rv)
@app.route('/home1')
def home1():
	return render_template('home1.py')
class RegisterForm(Form):
  name=StringField('Name',[validators.Length(min=1,max=50)])
  father_mother_name=StringField('father_mother_name',[validators.Length(min=4,max=50)])
  date_of_brith = DateField('date_of_brith', format='%Y-%m-%d')
  address=StringField('address',[validators.Length(min=1,max=50)])
  aadhar_number=StringField('aadhar_number',[validators.Length(min=1,max=50)])
  mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
  email=StringField('email',[validators.Length(min=2,max=50)])
  alternate_no=StringField('alternate_no',[validators.Length(min=6,max=50)])
  type1=SelectField(u'type',choices=[('None','None'),('FULLTIME','FULLTIME'),('PARTTIME','PARTTIME'),('INTENDS','INTENDS')])

@app.route('/register', methods = ['GET', 'POST'])
def register():
   form = RegisterForm(request.form)
   if request.method == 'POST' and form.validate():
       name = form.name.data
       father_mother_name = form.father_mother_name.data
       date_of_brith = form.date_of_brith.data
       address = form.address.data
       aadhar_number = form.aadhar_number.data
       mobile = form.mobile.data
       email = form.email.data
       alternate_no = form.alternate_no.data
       type1 = form.type1.data		
       # create cursor
       
       cur = mysql.connection.cursor()

       cur.execute("INSERT INTO employees(Name,Father_Mother_Name,Date_Brith,Address,Aadhar_number,Phone_number,Email_id,Alternate_no,Type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,father_mother_name,date_of_brith,address,aadhar_number,mobile,email,alternate_no,type1))
       mysql.connection.commit()
       #close connection
       cur.close()
       
       flash('You are now registered and can log in','success')
       
       return redirect(url_for('councling'))
   return render_template('register.html',form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM user1s WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('home111'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#-----------------------------------------login----------------
@app.route('/EMPlogin',methods = ['GET','POST'])
def EMPloginn():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE email = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('home111'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout1')
def EMPlogout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('EMPlogin'))
#--------------------------signup--------------------------------------------------
class Signup(Form):

  email=StringField('Reg_Email',[validators.Length(min=2,max=50)])
  password = PasswordField('password',[validators.Length(min=2,max=50)]) 
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
   form = Signup(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello') 
       
       email = form.email.data
       password = form.password.data
       cur=mysql.connection.cursor()
       cur.execute("SELECT Email FROM full_emps WHERE Email='"+email+"'")
       rv=cur.fetchall()
       print(email,"email")
       for x in rv:
        print(x['Email'])
        if(x['Email']==email):
          cur=mysql.connection.cursor()
          cur.execute("INSERT INTO users(email,password) VALUES(%s,%s)",(email,password))
          mysql.connection.commit()
          break
        else:
          print("plz enter correct email")
       return render_template('EMPlogin.html',rv=rv)
   return render_template('signup.html',form = form)
#--------------------------------forgot-------------------------------------------------
class Forgot(Form):
  DOB=StringField('DOB',[validators.Length(min=1,max=50)])
  fathername=StringField('fathername',[validators.Length(min=2,max=50)])
  email=StringField('email',[validators.Length(min=2,max=50)])
  password=PasswordField('password',[validators.Length(min=2,max=50)])
  
@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
   form = Forgot(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello') 
       DOB = form.DOB.data
       fathername = form.fathername.data
       email = form.email.data
       password = form.password.data
       cur=mysql.connection.cursor()
       cur.execute("SELECT Date_Brith,Email_id,Father_Mother_Name FROM employees WHERE Date_Brith=%s AND Father_Mother_Name=%s AND Email_id=%s",(DOB,fathername,email))
       rv=cur.fetchall()
       rv1=list(rv)

       if (DOB==rv1[0]['Date_Brith']):
        print(rv1[0]['Email_id'])
        cur.execute("SELECT * FROM users WHERE email='"+rv1[0]['Email_id']+"'")
        rv2=cur.fetchall()
        rv3=list(rv2)
        print(rv3[0]['email'])
        cur.execute("UPDATE `users` SET `password`=%s WHERE email=%s",[password,email])
        mysql.connection.commit()

       return render_template('login.html',rv=rv)
   return render_template('forgot.html',form = form)
#--------------------------signup-admin--------------------------------------------------
class Signupa(Form):
  emp_id=StringField('Emp_id',[validators.Length(min=1,max=50)])
  email=StringField('Email',[validators.Length(min=2,max=50)])
  password = PasswordField('password',[validators.Length(min=2,max=50)]) 
@app.route('/signupa', methods = ['GET', 'POST'])
def signupa():
   form = Signupa(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print('hello') 
       emp_id = form.emp_id.data
       email = form.email.data
       password = form.password.data
       return render_template('login.html',rv=rv)
   return render_template('signupa.html',form = form)
#---------------------------------------------------------------------------------

@app.route('/updateprofile')
def updateprofile():
  id=request.args.get('id')
  print('updateproile::',id)
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE id=%s",[id])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  return render_template('update.html',person=person)

@app.route('/updateprofile12')
def updateprofile12():
  name=request.args.get('st_name')
  email=request.args.get('st_email')
  
  cur=mysql.connection.cursor()
  cur.execute("SELECT id,st_name,st_email FROM registers WHERE st_name=%s",[name])
  rv=cur.fetchall()
  person=rv[0]
  print(person)
  a=person['id']
  print(person['email'])


  cur=mysql.connection.cursor()
  cur.execute("UPDATE `registers` SET `name`=%s,`email`=%s WHERE id=%s",[name,email,a])
  print(name)
  print(email)
  print(a)
  mysql.connection.commit()

  return redirect(url_for('about'))

@app.route('/deleteprofile')
def deleteprofile():
  id=request.args.get('id')
  print("delect",id)
  cur=mysql.connection.cursor()
  cur.execute("DELETE FROM `users`  WHERE id=%s",[id])
  mysql.connection.commit()
 
  return redirect(url_for('about'))


if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=5000, debug=True)

