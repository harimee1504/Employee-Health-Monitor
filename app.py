from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import random

app = Flask(__name__)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Your User Name",
    password="Your Password",
    hostname="Your Hostname",
    databasename="Your Database Name",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

USER_DATA = {
    "name": "Your User Name", "password": "Your Password"
}


def execute(query):
    t = text(query)
    result = db.session.execute(t)
    res = result.fetchall()
    return res


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/mob')
def mobindex():
    return render_template('moblogin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        if name.lower() == USER_DATA["name"].lower() and pwd == USER_DATA["password"]:
            return redirect(url_for('details'), code=307)
        return redirect('/')
    return redirect('/')


@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        name = request.form["name"]
        pwd = request.form["pass"]
        na = 'SELECT password from '+name
        try:
            na = execute(na)
        except:
            return render_template("notfound.html", msg="OOPS! USER DOES NOT EXISTS")
        newpwd = str(na[0][0])
        if pwd == newpwd:
            return redirect(url_for('health'), code=307)
        return render_template("notfound.html", msg="Incorrect Password")
    return redirect('/')


@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == "POST":
        a = execute('show tables')
        res = []
        for i in a:
            te = str(i)
            res.append(te[2:-3])
        c = 0
        ite = []
        for i in res:
            c += 1
            fn = 'SELECT fname FROM '+i
            ln = 'SELECT lname FROM '+i
            jo = 'SELECT job FROM '+i
            fn = execute(fn)
            ln = execute(ln)
            jo = execute(jo)
            fn1, ln1, jo1 = [], [], []
            for k in range(len(fn)):
                for j in fn[k].values():
                    fn1.append(j)
                for j in ln[k].values():
                    ln1.append(j)
                for j in jo[k].values():
                    jo1.append(j)
            temp = [c, fn1, ln1, jo1, i]
            ite.append(temp)
        return render_template('result.html', ite=ite, n=len(ite))
    return redirect('/')


@app.route('/sdetails', methods=['GET', 'POST'])
def sdetails():
    if request.method == "POST":
        name = request.form["name"]
        res = 'SELECT * FROM '+name
        res = execute(res)
        det = [res[0][0]+' '+res[0][1], res[0][2],
               res[0][3], res[0][4], res[0][5], res[0][6]]

        req = urllib.request.Request(
            "http://blynk-cloud.com/9RrVUXGZV5MYo7lTBhus1KsFrKt4iruW/get/V8")
        req1 = urllib.request.Request(
            "http://blynk-cloud.com/9RrVUXGZV5MYo7lTBhus1KsFrKt4iruW/get/V7")
        bpo2 = urllib.request.urlopen(req).read()
        spo2 = urllib.request.urlopen(req).read()

        return render_template('details.html', det=det, bpm=bpm, spo2=spo2)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        uname = request.form["uname"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        age = request.form["age"]
        gender = request.form["gender"]
        height = request.form["height"]
        wei = request.form["weight"]
        job = request.form["job"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        token = request.form["token"]
        try:
            query = "CREATE TABLE "+uname + \
                " (fname VARCHAR(50),lname VARCHAR(50),age VARCHAR(3),gender VARCHAR(10),height VARCHAR(5),weight VARCHAR(5),job VARCHAR(50),phone VARCHAR(15),beat VARCHAR(15),spo2 VARCHAR(15),time VARCHAR(50),email VARCHAR(30),password VARCHAR(30),token VARCHAR(50))"
            table = text(query)
            db.session.execute(table)
            db.session.commit()
        except:
            return render_template("notfound.html", msg="User Name Already Exists !")
        table = text("INSERT INTO "+uname+" (fname,lname,age,gender,height,weight,job,phone,email,password,token) VALUES(:fname,:lname,:age,:gender,:height,:weight,:job,:phone,:email,:password,:token)")\
            .bindparams(fname=fname, lname=lname, age=age, gender=gender, height=height, weight=wei, job=job, phone=phone, email=email, password=password, token=token)
        db.session.execute(table)
        db.session.commit()
        return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Employee Details</title><link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap"rel="stylesheet"/></head><body style="background:#282828;color:e0e0e0;"><div style="display: flex;flex-direction:column;height: 100vh;justify-content: center;align-items: center;"><h1 style="color: #c9c0c0;">Registration Successful</h1><form><a href="/mob"style="padding:20px 40px;text-decoration:none;background:#126cce;border-radius:8px;color:e0e0e0;cursor:pointer;">Go back!</a></form></div></body></html>'
    return redirect('/')


@app.route('/health', methods=['GET', 'POST'])
def health():
    bpm = random.randint(78, 99)
    spo2 = random.randint(90, 125)
    return render_template('mobdetail.html', bpm=bpm, spo2=spo2)


@app.route('/reg')
def reg():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
