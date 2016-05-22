from flask import Flask, render_template, session, request, redirect
import database, hashlib
import json


app = Flask(__name__)

@app.route("/")
def index():
    with open('../secret_key/gmail.json') as data_file:
        data = json.load(data_file)
    client_id = data['web']['client_id']
    return render_template("index.html", username = session.get('username'), client_id = client_id)

@app.route('/add_user')
def addUser():
    username = request.args.get('username', 0, type=str)
    email = request.args.get('email', 0, type=str)
    print username
    print email
    session['username'] = username
    return redirect("/")

@app.route("/testLogin", methods=["GET", "POST"])
def testLogin():
    if request.method == "GET":
        if session.get('username') != None:
            return redirect("/")
        else:
            return render_template("login.html", username = None)
    else:
        username = request.form.get("login")
        session['username'] = username
        return redirect("/")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "supersecretkey"
    app.run(host = '0.0.0.0', port = 8000)
