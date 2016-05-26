from flask import Flask, render_template, session, request, redirect
import database
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open('../secret_key/gmail.json') as data_file:
        data = json.load(data_file)
    client_id = data['web']['client_id']
    return render_template("index.html", username = session.get('username'), auth = session.get('auth'), client_id = client_id)

@app.route('/addUser')
def addUser():
    if len(request.args.keys()) != 0:
        session['username'] = request.args.get('username', 0, type=str)
        session['email'] = request.args.get('email', 0, type=str)
        session['auth'] = request.args.get('auth', 0, type=str)
        if session.get('auth') == 'teacher':
            database.create_teacher(session.get('username'), session.get('email'))
        else:
            database.create_student(session.get('username'), session.get('email'))
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/classes")
@app.route("/classes/<class_id>", methods=["GET", "POST"])
def classes(class_id = ""):
    if len(class_id) < 1:
        if session.get('auth') != 'teacher':
            return redirect("/")
        else:
            return render_template("classes.html", username = session.get('username'), auth=session.get('auth'), classes = database.find_classes(session.get('email')))
    else:
        c1 = database.find_class(class_id)
        if c1 == None:
            return redirect("/")
        if request.method == "GET":
            return render_template("class.html", username = session.get('username'), auth=session.get('auth'), class_one = c1, students = database.all_students_in_class(class_id))
        if request.method == "POST":
            button = request.form['button']
            if button == "Enroll in Class":
                print class_id
                database.add_to_class(session.get('email'), class_id)
                return redirect("/classes/"+class_id)
            if button == "Leave Class":
                database.remove_from_class(session.get('email'), class_id)
                return redirect("/classes/"+class_id)
            if button == "Email Multiple Students":
                return redirect("/sendMail/"+class_id)

@app.route("/createClass", methods=["GET", "POST"])
def createClass():
    if request.method == "GET":
        if session.get('auth') != 'teacher':
            return redirect("/")
        else:
            return render_template("createClass.html", username = session.get('username'), auth = session.get('auth'), email = session.get('email'))
    else:
        database.create_class(session.get('username'), session.get('email'), request.form.get('course_code'), request.form.get('course_name'), request.form.get('course_period'))
        return redirect("/")

@app.route("/contactInfo", methods=["GET", "POST"])
def contactInfo():
    if request.method == "GET":
        if session.get('auth') != 'student':
            return redirect("/")
        else:
            return render_template("contactInfo.html", username = session.get('username'), auth = session.get('auth'), email = session.get('email'), student = database.check_contact_info(session.get('email')))
    else:
        database.add_contact_info(session.get('email'), request.form.get('sname'), request.form.get('sphone'), request.form.get('address'), request.form.get('pname'), request.form.get('pphone'), request.form.get('pemail'), request.form.get('gname'), request.form.get('gphone'), request.form.get('gemail'))
        return redirect("/")

@app.route("/addClasses", methods=["GET", "POST"])
def addClasses():
    if request.method == "GET":
        if session.get('auth') != 'student':
            return redirect("/")
        else:
            return render_template("addClass.html", username = session.get('username'), auth = session.get('auth'), email = session.get('email'))
    else:
        button = request.form['button']
        if button == "Look":
            checked = request.form.getlist("checks")
            return render_template("addClass.html", username = session.get('username'), auth = session.get('auth'), email = session.get('email'), classes = database.all_classes_in_period(checked))
        else:
            return render_template("addClass.html", username = session.get('username'), auth = session.get('auth'), email = session.get('email'))#,database.all_classes_in_period())
    return redirect("/")

@app.route("/sendEmail")
def sendEmail():
    return render_template("sendMail.html")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "supersecretkey"
    app.run(host = '0.0.0.0', port = 8000)
