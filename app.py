from flask import Flask, render_template, session, request, redirect
import database, hashlib

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("/index.html", current_user = session.get('username'), auth = session.get('auth'))

@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "GET":
        if session.get('username') != None:
            return redirect("/")
        else:
            return render_template("/login.html")
    else:
        username = request.form.get("login")
        session['username'] = username
        session['auth'] = 'teacher'
        return redirect("/")
        
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "GET":
        if session.get('user') != None:
            return redirect("/")
        else:
            return render_template("/login.html")
    else:
        username = request.form.get("login")
        session['user'] = username
        session['auth'] = 'student'
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    
if __name__ == "__main__":
    app.debug = True
    app.secret_key = "supersecretkey"
    app.run(host = '0.0.0.0', port = 8000)
