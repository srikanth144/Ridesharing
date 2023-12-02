from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import requests

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb ;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cdd46291;PWD=PRXIWbfPAOOEGBiM;", '', '')

print("conn")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/a')
def login():
    return render_template("login.html")

@app.route('/b')
def register():
    return render_template("register.html")

@app.route('/submit1',methods=['POST'])
def register1():
    x = [x for x in request.form.values()]
    print(x)
    Name=x[0]
    Email=x[1]
    MobileNo=x[2]
    Password = x[3]
    sql = "SELECT * FROM REGISTER WHERE Email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,Email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('login.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, Name)
        ibm_db.bind_param(prep_stmt, 2, Email)
        ibm_db.bind_param(prep_stmt, 3, MobileNo)
        ibm_db.bind_param(prep_stmt, 4, Password)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', pred="Registration Successful, please login using your details")
    


@app.route('/submit',methods=['POST'])
def login1():
    Email = request.form['Email']
    Password = request.form['Password']
    sql = "SELECT * FROM REGISTER WHERE Email =? AND Password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,Email)
    ibm_db.bind_param(stmt,2,Password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(Email,Password)
    if account:
            return render_template('login.html', pred="Login successful")
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username/password !") 

if __name__ == "__main__":
    app.run(debug = True,port = 5000)