import sqlite3
import database as d
from flask import Flask,request,render_template,redirect,url_for
conn=None
login=False
app=Flask(__name__)

@app.route('/')
def index():
	global conn
	conn=d.default_data()
	return render_template("edutech.html")

@app.route('/signup')
def index1():
	return render_template("signup.html")

@app.route('/edutech/<option>', methods=['post','get'])
def index3(option):
	global conn,login
	if option=="login":
		m=request.form.get("mail")
		p=request.form.get("password")
		name,status=d.login(conn,m,p)
		if status==1:
			login=True
			c="green"
			m=name+" ,You have Successfully Logged in..."
		elif status==2:
			c="red"
			m="Wrong Password"
		else:
			c="red"
			m="Wrong E-Mail or Click on Sign Up to Create Account"
	else:
		n=request.form.get("name")
		m=request.form.get("mail")
		p1=request.form.get("password")
		p2=request.form.get("password-repeat")
		if p1==p2:
			name,status=d.signup(conn,n,m,p1)
			if status==1:
				login=True
				m=name+" ,You have Successfully Created Account..."
				c="green"
			elif status==2:
				c="red"
				m=name+" , Your Account already exists ... Click on Log In Button"
		else:
			m="Passwords don't match ... Give Same Passwords"
			c="red"
	return render_template("edutech.html",message=m,color=c)

@app.route('/login')
def index2():
	return render_template("login.html")

@app.route('/question')
def index4():
	return render_template("question.html")

@app.route('/submit_questions',methods=['post'])
def index5():
	question=request.form.get('question')
	return render_template("submit_questions.html")


if __name__=='__main__':
	app.run(debug=True)
