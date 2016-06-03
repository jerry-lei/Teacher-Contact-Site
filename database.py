from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

connection = MongoClient()
db = connection['database']

def create_student(student_name, student_email):
    students = db['students']
    if students.find_one({'student_email': student_email}) == None:
        new_student = {'student_name': student_name,
                       'student_email': student_email,
                       'preferred_name': '',
                       'student_phone': '',
                       'address': '',
                       'parent_name': '',
                       'parent_phone': '',
                       'parent_email': '',
                       'counselor_name': '',
                       'counselor_phone': '',
                       'counselor_email': ''}
        students.insert_one(new_student)

def check_contact_info(student_email):
    students = db['students']
    student = students.find_one({'student_email': student_email})
    return student

def add_contact_info(student_email, preferred_name, student_phone, address, parent_name, parent_phone, parent_email, counselor_name, counselor_phone, counselor_email):
    students = db['students']
    students.find_one_and_update({'student_email': student_email},
                                 {'$set':{'preferred_name': preferred_name,
                                  'student_phone': student_phone,
                                  'address': address,
                                  'parent_name': parent_name,
                                  'parent_phone': parent_phone,
                                  'parent_email': parent_email,
                                  'counselor_name': counselor_name,
                                  'counselor_phone': counselor_phone,
                                  'counselor_email': counselor_email}})

def create_teacher(teacher_name, teacher_email):
    teachers = db['teachers']
    if teachers.find_one({'teacher_email': teacher_email}) == None:
        new_teacher = {'teacher_name': teacher_name,
                     'teacher_email': teacher_email}
        teachers.insert_one(new_teacher)

def create_class(teacher_name, teacher_email, course_code, class_name, class_period):
    classes = db['classes']
    new_class = {'teacher_name': teacher_name,
                 'teacher_email': teacher_email,
                 'course_code': course_code,
                 'class_name': class_name,
                 'class_period': class_period,
                }
    classes.insert_one(new_class)
    teachers = db['teachers']
    teachers.find_one_and_update({'teacher_email': teacher_email},
                                 {'$push':{'classes': ObjectId(new_class.get('_id'))}})

def delete_class(class_id):
    teachers = db['teachers']
    classes = db['classes']
    students = db['students']
    c = classes.find_one({'_id': ObjectId(class_id)})
    teachers.find_one_and_update({'teacher_email': c.get('teacher_email')},
                                {'$pull':{'classes': ObjectId(class_id)}})
    if c.get('students') != None:
        for x in c.get('students'):
            students.find_one_and_update({'student_email': x}, {'$pull': {'classes': ObjectId(class_id)}})

def find_student_classes(student_email):
    students = db['students']
    classes = db['classes']
    allClasses = []
    classIds = students.find_one({'student_email': student_email}).get('classes')
    if classIds != None:
        for x in classIds:
            allClasses.append(classes.find_one({'_id': ObjectId(x)}))
    return allClasses
            
def find_teacher_classes(teacher_email):
    classes = db['classes']
    return classes.find({'teacher_email': teacher_email})

def find_class(class_id):
    classes = db['classes']
    ret_class = classes.find_one({'_id': ObjectId(class_id)})
    return ret_class

def all_classes_in_period(class_periods): #class_period in string form (array to allow multiple checkboxes)
    classes = db['classes']
    class_by_period = []
    for x in xrange(len(class_periods)):
        class_by_period.append(class_periods[x][1:])
    return classes.find({'class_period': {"$in": class_by_period}})

def classes_student_in(student_email):
    pass

def add_to_class(student_email, class_id):
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                {'$addToSet': {'students': student_email}})
    students = db['students']
    students.find_one_and_update({'student_email': student_email},
                                 {'$addToSet': {'classes': ObjectId(class_id)}})

def remove_from_class(student_email, class_id):
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                {'$pull': {'students': student_email}})
    students = db['students']
    students.find_one_and_update({'student_email': student_email},
                                 {'$pull': {'classes': ObjectId(class_id)}})
    
def all_students_in_class(class_id):
    students = []
    emails = db['classes'].find_one({'_id': ObjectId(class_id)}).get('students')
    if emails == None:
        return {}
    for email in emails:
        students.append(db['students'].find_one({'student_email': email}))
    return students

def add_log(teacher_name, student_name):
  logs = db['logs']
  time = datetime.now()
  new_log = {'teacher_name': teacher_name,
             'student_name': student_name,
             'time': str(time),
             'notes':''
            }
  logs.insert_one(new_log)

def find_log(teacher_name):
  logs = db['logs']
  return logs.find({'teacher_name': teacher_name})

def delete_log(teacher_name,student_name,time):
  logs = db['logs']
  teacher_logs = logs.find({'teacher_name': teacher_name})
  log_by_student = []
  for item in teacher_logs:
    if item['student_name'] == student_name:
      log_by_student.append(item)
  log_by_time = []
  for item in log_by_student:
    if item['time'] == time:
      log_by_time.append(item)
  return logs.remove({'_id': ObjectId(log_by_time[0]['_id'])})

def add_to_log(teacher_name,student_name,time,notes):
    logs = db['logs']
    logs.find_one_and_update({'_id' : ObjectId(time)},
                             {'$addToSet': {'notes': notes}})


