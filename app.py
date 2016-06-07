from flask import Flask, render_template, session, request, redirect, jsonify
import database
import utils
import json
import cgi

app = Flask(__name__)

with open('gmail.json') as data_file:
    data = json.load(data_file)
client_id = data['web']['client_id']

@app.route("/")
def index():
    return render_template("index.html", client_id = client_id, username = session.get('username'), auth = session.get('auth'))

@app.route('/addUser')
def addUser():
    if request.is_xhr:
        session['username'] = request.args.get('username', 0, type=str)
        session['email'] = request.args.get('email', 0, type=str)
        session['auth'] = request.args.get('auth', 0, type=str)
        if session.get('auth') == 'teacher':
            database.create_teacher(session.get('username'), session.get('email'))
        else:
            database.create_student(session.get('username'), session.get('email'))
        return jsonify()
    return redirect("/")

@app.route("/logout")
def logout():
    if request.is_xhr:
        session.clear()
        return jsonify()
    return redirect("/")

@app.route("/myClasses")
def myClasses():
    if session.get('auth') != 'student':
        return redirect("/")
    else:
        return render_template("classes.html",client_id = client_id, username = session.get('username'), auth=session.get('auth'), classes = database.find_student_classes(session.get('email')))

@app.route("/classes")
@app.route("/classes/<class_id>", methods=["GET", "POST"])
def classes(class_id = ""):
    if len(class_id) < 1:
        if session.get('auth') != 'teacher':
            return redirect("/")
        else:
            return render_template("classes.html",client_id = client_id, username = session.get('username'), auth=session.get('auth'), classes = sorted(database.find_teacher_classes(session.get('email')), key=lambda x: x.get('class_period')))
    else:
        c1 = database.find_class(class_id)
        if c1 == None or session.get('auth') == None:
            return redirect("/")
        if request.method == "GET":
            return render_template("class.html",client_id = client_id, username = session.get('username'), auth=session.get('auth'), class_one = c1, students = sorted(database.all_students_in_class(class_id), key=lambda x: x.get('student_name').split()[-1]))
        else:
            button = request.form['button']
            if button == "Enroll in Class":
                database.add_to_class(session.get('email'), class_id)
                return redirect("/classes/"+class_id)
            if button == "Leave Class":
                database.remove_from_class(session.get('email'), class_id)
                return redirect("/classes/"+class_id)
            if button == "Email Multiple Students":
                return redirect("/sendMail/"+class_id)
            if button == "Confirm Delete":
                print "HERE!"
                database.delete_class(class_id)
                return redirect("/classes")

@app.route("/sendMail/<class_id>", methods=["GET","POST"])
def sendMail(class_id):
    c1 = database.find_class(class_id)
    if c1 == None or session.get('auth') == None:
        return redirect("/")
    if request.method == "GET":
        return render_template("sendMail.html",client_id = client_id, username = session.get('username'), auth=session.get('auth'), class_one = c1, students = database.all_students_in_class(class_id))
    elif request.method == "POST":
        print "ASDFASDF"
        button = request.form['button']
        formData=cgi.FieldStorage()
        if 'checkbox' in formData and formData.getvalue('checkbox') == 'on':
            template = request.form['checkbox']
        else:
            template = ''
        #database.log_mail (FUNCTION THAT CLIENT ASKED FOR)
        if button == "Go to Email Page":
            to = request.form.getlist("checks")
            body = request.form.get("body_name")
            subject = request.form.get("subject_name")
            teacher_name = session.get('username')
            gmail_link = utils.make_link(body, to, subject, template, teacher_name)
            for student in request.form.getlist("checks"):
                database.add_log(session.get('username'),student)
            return redirect(gmail_link)

@app.route("/createClass", methods=["GET", "POST"])
def createClass():
    if request.method == "GET":
        if session.get('auth') != 'teacher':
            return redirect("/")
        else:
            return render_template("createClass.html",client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'))
    else:
        database.create_class(session.get('username'), session.get('email'), request.form.get('course_code'), request.form.get('course_name'), str(request.form.get('course_period')))
        return redirect("/classes")

@app.route("/contactInfo", methods=["GET", "POST"])
@app.route("/contactInfo/<student_id>", methods=["GET", "POST"])
def contactInfo(student_id=""):
    if request.method == "GET":
        if session.get('auth') == 'student':
            if len(student_id) > 0:
                return redirect("/contactInfo")
            else:
                return render_template("contactInfo.html", client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'), student = database.find_student(session.get('email')))
        elif session.get('auth') == 'teacher':
            if database.find_student(student_id) == None:
                return redirect("/")
            else:
                return render_template("contactInfo.html", client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'), student = database.find_student(student_id))
        else:
            return redirect("/")
    else:
        if session.get('auth') == 'student':
            database.add_contact_info(session.get('email'), request.form.get('sname'), request.form.get('sphone'), request.form.get('address'), request.form.get('pname'), request.form.get('pphone'), request.form.get('pemail'), request.form.get('gname'), request.form.get('gphone'), request.form.get('gemail'))
        elif session.get('auth') == 'teacher':
            database.add_contact_info(student_id, request.form.get('sname'), request.form.get('sphone'), request.form.get('address'), request.form.get('pname'), request.form.get('pphone'), request.form.get('pemail'), request.form.get('gname'), request.form.get('gphone'), request.form.get('gemail'))
        return redirect("/")

@app.route("/addClasses", methods=["GET", "POST"])
def addClasses():
    if request.method == "GET":
        if session.get('auth') != 'student':
            return redirect("/")
        else:
            return render_template("addClass.html",client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'))
    else:
        button = request.form['button']
        if button == "Look":
            checked = request.form.getlist("checks")
            return render_template("addClass.html",client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'), classes = database.all_classes_in_period(checked))
        else:
            return render_template("addClass.html",client_id = client_id, username = session.get('username'), auth = session.get('auth'), email = session.get('email'))#,database.all_classes_in_period())
    return redirect("/")

@app.route("/log")
@app.route("/log/<logId>", methods=["GET", "POST"])
def log(logId = ""):
    if session.get('auth') != 'teacher':
        return redirect("/")
    else:
        if len(logId) == 0:
            return render_template("log.html",client_id = client_id, username = session.get('username'), auth=session.get('auth'), logs = database.find_all_logs(session.get('username')))
        elif database.find_log(logId) == None:
            return redirect("/log")
        elif request.method == "GET":
            return render_template("logInfo.html", log = database.find_log(logId), client_id = client_id, username = session.get('username'), auth=session.get('auth'))
        else:
            database.add_to_log(logId, request.form.get('notes'))
            return redirect("/log/"+logId)
'''
@app.route("/templates")
def templates():
    return render_template("templates.html", client_id = client_id, username = session.get('username'), auth=session.get('auth'))
'''

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "supersecretkey"
    app.run(host = '0.0.0.0', port = 8000)
