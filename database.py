from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

connection = MongoClient()
db = connection['database']

def create_student(student_name, student_email):
    """
    Creates a document in db['students']. Happens upon first login.
    Parameters:
        String student_name
        String student_email
    """
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

def find_student(student_email):
    """
    Query with student_email.
    Parameters:
        String student_email
    Returns:
        cursor
    """
    students = db['students']
    student = students.find_one({'student_email': student_email})
    return student

def add_contact_info(student_email, preferred_name, student_phone, address, parent_name, parent_phone, parent_email, counselor_name, counselor_phone, counselor_email):
    """
    Creates a document in db['teachers']. Happens upon first login.
    Parameters:
        String student_name
        String student_email
    """
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
    """
    Creates a document in db['teachers']. Happens upon first login.
    Parameters:
        String teacher_name
        String teacher_email
    """
    teachers = db['teachers']
    if teachers.find_one({'teacher_email': teacher_email}) == None:
        new_teacher = {'teacher_name': teacher_name,
                     'teacher_email': teacher_email}
        teachers.insert_one(new_teacher)

def create_class(teacher_name, teacher_email, course_code, class_name, class_period):
    """
    Creates a document in db['classes'] (Access only by teacher). Adds the class to the teacher's list of classes.
    Parameters:
        String teacher_name
        String teacher_email
        String course_code
        String class_name
        String class_period
    """
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
    """
    Deletes a class by its class_id. Removes from student's, and teacher's list of classes.
    Parameters:
        String class_id
    """
    teachers = db['teachers']
    classes = db['classes']
    students = db['students']
    c = classes.find_one({'_id': ObjectId(class_id)})
    teachers.find_one_and_update({'teacher_email': c.get('teacher_email')},
                                {'$pull':{'classes': ObjectId(class_id)}})
    if c.get('students') != None:
        for x in c.get('students'):
            students.find_one_and_update({'student_email': x}, {'$pull': {'classes': ObjectId(class_id)}})
    classes.remove({'_id': ObjectId(class_id)})

def find_student_classes(student_email):
    """
    Find all classes that a student is enrolled in.
    Parameters:
        String student_email
    Returns:
        cursor[]
    """
    students = db['students']
    classes = db['classes']
    allClasses = []
    classIds = students.find_one({'student_email': student_email}).get('classes')
    if classIds != None:
        for x in classIds:
            allClasses.append(classes.find_one({'_id': ObjectId(x)}))
    return allClasses

def find_teacher_classes(teacher_email):
    """
    Find all classes that are created by a teacher.
    Parameters:
        String teacher_email
    Returns:
        cursor[]
    """
    classes = db['classes']
    return classes.find({'teacher_email': teacher_email})

def find_class(class_id):
    """
    Returns document from collection 'classes' from ObjectId.
    Parameters:
        String class_id
    Returns:
        cursor
    """
    classes = db['classes']
    ret_class = classes.find_one({'_id': ObjectId(class_id)})
    return ret_class

def all_classes_in_period(class_periods):
    """
    Returns documents from db['classes'] where the 'class_period' key is equal to the values in the array 'class_periods'.
    Parameters:
        str[] class_periods
            ex. ['p1','p2','p6'] -- names in the checkbox
    Returns:
        cursor[]
    """
    classes = db['classes']
    class_by_period = []
    for x in xrange(len(class_periods)):
        class_by_period.append(class_periods[x][1:])
    return classes.find({'class_period': {"$in": class_by_period}})

def add_to_class(student_email, class_id):
    """
    Adds student to class. Adds class to student.
    Parameters:
        String student_email
        String class_id
    """
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                {'$addToSet': {'students': student_email}})
    students = db['students']
    students.find_one_and_update({'student_email': student_email},
                                 {'$addToSet': {'classes': ObjectId(class_id)}})

def remove_from_class(student_email, class_id):
    """
    Removes student from class. Removes class from student.
    Parameters:
        String student_email
        String class_id
    """
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                {'$pull': {'students': student_email}})
    students = db['students']
    students.find_one_and_update({'student_email': student_email},
                                 {'$pull': {'classes': ObjectId(class_id)}})

def all_students_in_class(class_id):
    """
    Returns a list of all students that are enrolled in a class.
    Parameters:
        String class_id
    Returns:
        cursor[]
    """
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
