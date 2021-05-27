from flask import *  
import sqlite3  
  
app = Flask(__name__) 
app.secret_key = "Secret key"  
 
@app.route("/")  
def index():  
    return render_template("index.html");  
 
 
@app.route("/newacc",methods = ["POST","GET"])  
def newacc():  
    msg = ""  
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            email = request.form["email"]  
            password = request.form["password"]  
            with sqlite3.connect("user.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Users (name, email, password) values (?,?,?)",(name,email,password))  
                con.commit()  
                msg = "Hey! Your account is created successfully"  
        except:  
            con.rollback()  
            msg = "Oops! User already exists"  
        finally:  
            return render_template("index.html",msg = msg)  
            con.close()
    return render_template('index.html')
 
 
@app.route("/login",methods = ["POST","GET"])  
def login():  
    msg = "" 
    if request.method == "POST":  
        email = request.form["email"]  
        password = request.form["password"]  
        with sqlite3.connect("user.db") as con:
            con.row_factory = sqlite3.Row   
            cur = con.cursor()  
            cur.execute("SELECT * FROM Users WHERE email = ? AND password = ?",(email, password)) 
            info = cur.fetchall()   
        if info:
            session['loggedin'] = True
            session['email'] = email
            return render_template('home.html',info=info)
        else:
            msg = 'Incorrect email or password!'
    return render_template('login.html', msg = msg) 

  
 
  
if __name__ == "__main__":  
    app.run(debug = True)  