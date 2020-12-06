import random
import sqlite3
global conn

def default_data():
	conn = sqlite3.connect("edutech.db")
	conn.execute('''CREATE TABLE IF NOT EXISTS users
    	    (uid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	    uname		VARCHAR(50) NOT NULL,
    	    umail		TEXT NOT NULL UNIQUE,
    	    password	TEXT NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS teachers
    	     (tid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     tname		VARCHAR(50) NOT NULL,
    	     tmail		VARCHAR(40) NOT NULL UNIQUE,
    	     degree		VARCHAR(10) NOT NULL,
    	     rating		INTEGER NOT NULL,		
    	     time_taken	REAL NOT NULL);''')	

	conn.execute('''CREATE TABLE IF NOT EXISTS boards
    	     (bid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     bname		VARCHAR(50) NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS subjects
    	     (sid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     sname		VARCHAR(50) NOT NULL,
    	     rating		INTEGER NOT NULL,		
    	     price		INTEGER NOT NULL);''')	

	conn.execute('''CREATE TABLE IF NOT EXISTS registered
    	     (rid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     sid		INTEGER NOT NULL REFERENCES subjects(sid),
    	     uid		INTEGER NOT NULL REFERENCES users(uid));''')    

	conn.execute('''CREATE TABLE IF NOT EXISTS classes
    	     (cid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     cname		VARCHAR(50) NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS handled
    	     (hid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     tid		INTEGER NOT NULL REFERENCES teachers(tid),
    	     cid		INTEGER NOT NULL REFERENCES classes(cid),
    	     sid		INTEGER NOT NULL REFERENCES subjects(sid));''')

	conn.execute('''CREATE TABLE IF NOT EXISTS contains
    	     (conid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     bid		INTEGER NOT NULL REFERENCES boards(bid),
    	     cid		INTEGER NOT NULL REFERENCES classes(cid));''')

	conn.execute('''CREATE TABLE IF NOT EXISTS offers
			(ofid		INTEGER PRIMARY KEY AUTOINCREMENT,
			conid		INTEGER NOT NULL REFERENCES contains(conid),
    	     sid		INTEGER NOT NULL REFERENCES subjects(sid),
    	     chapters	INTEGER NOT NULL);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS questions
    	     (qid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     question	VARCHAR(500),
    	     photo_path	VARCHAR(100));''')			#path to the photo uploaded by the user

	conn.execute('''CREATE TABLE IF NOT EXISTS asigned
    	     (aid		INTEGER PRIMARY KEY AUTOINCREMENT,
    	     qid		INTEGER NOT NULL REFERENCES questions(qid),
    	     uid		INTEGER NOT NULL REFERENCES users(uid),
    	     tid		INTEGER NOT NULL REFERENCES teachers(tid)),
    	     status		VARCHAR(15) NOT NULL CHECK (status='assigned' or status='solved' or status='wrong qustion'),
    	     assign_time	datetime NOT NULL,
    	     solved_time	datetime);''')

	classes=["VII","VIII","IX","X"]
	subjects=["Physics","Chemistry","Mathematics","Computer Science","Economics",
	"Accountancy","Biology","History","Geography","Java","Python","Database Management System"]
	teachers=["M G Aditya","L Chinmay","Manaswini","Manjunath S","Mansi M","Jhonson Furtado",
	"M B Raghav","Prithvi Raghavan","Rahul Krupani","Rahul M","Rohit B M","Naveen V"]
	tmail=[i.lower().replace(" ","")+"@gmail.com" for i in teachers]
	degree=["M.Sc","M.Tech, PHD","MS","B.Sc","B.Tech"]
	boards=["CBSE","Assam","Himachal Pradesh","Tamil Nadu","Maharashtra","Delhi"]

	#insert records into classes table
	for i in range(4):
		conn.execute("INSERT INTO classes (cname) VALUES(?)",(classes[i],))

	#insert records into teachers table
	for i in range(12):
		conn.execute("INSERT INTO teachers(tname,tmail,degree,rating,time_taken) \
		VALUES(?,?,?,?,?)",(teachers[i],tmail[i],random.choice(degree),round(random.uniform(3.0,5.0),2),random.randint(30,120)))
	#insert records into subjects/course table
		conn.execute("INSERT INTO subjects (sname,rating,price) \
		VALUES(?,?,?)",(subjects[i],round(random.uniform(3.0,5.0),2),random.randint(2500,7000)))
	#which subject is handles by which teacher for which class
		for j in range(4):
			conn.execute("INSERT INTO handled (tid,cid,sid) VALUES \
			(?,?,?)",(random.randint(1,12),j,i))

	#all boards contains class VII,VIII,IX,X
	k=1
	for i in range(6):
	#insert records into boards table
		ind=random.sample(range(1,12),6)
		conn.execute("INSERT INTO boards(bname) VALUES(?)",(boards[i],))
		for j in range(4):
			conn.execute("INSERT INTO contains (bid,cid) VALUES\
			(?,?)",(i,j))
			conn.execute("INSERT INTO offers(conid,sid,chapters) \
			VALUES (?,?,?)",(k,ind[(k%6)-1 if k%6!=0 else 5],random.randint(8,17)))
			k+=1
	conn.commit()
	print(conn)
	return conn

def login(conn,mail,password):
	cursor=conn.cursor()
	cursor.execute("SELECT uname,umail,password from users where umail=(?)",(mail,))
	r=cursor.fetchone()
	if r==None or len(r)==0:
		return "",3
	else:
		if r[1]==mail and r[2]!=password:
			return r[0],2
		elif r[1]==mail and r[2]==password:
			return r[0],1

def signup(conn,name,mail,password):
	cursor=conn.cursor()
	cursor.execute("SELECT uname,umail,password from users where umail=(?)",(mail,))
	r=cursor.fetchone()
	if r==None or len(r)==0:
		conn.execute("INSERT INTO users (uname,umail,password) \
		VALUES(?,?,?)",(name,mail,password))
		conn.commit()
		return name,1
	else:
		return name,2