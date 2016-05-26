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
    db['teachers'].find_one_and_update({'teacher_email': teacher_email},
                                 {'$push':{'classes': new_class.get('_id')}})
def delete_class(class_id):
    classes = db['classes']
    return classes.remove({'_id': ObjectId(class_id)})
    
def find_classes(teacher_email):
    classes = db['classes']
    return classes.find({'teacher_email': teacher_email})

def find_class(class_id):
    classes = db['classes']
    #return classes.find_one({'_id': class_id})
    ret_class = classes.find_one({'_id': ObjectId(class_id)})
    return ret_class

def all_classes_in_period(class_periods): #class_period in string form (array to allow multiple checkboxes)
    classes = db['classes']
    class_by_period = []
    for x in xrange(len(class_periods)):
        class_by_period.append(class_periods[x][1:])
    return classes.find({'class_period': {"$in": class_by_period}})

#print all_classes_in_period(['p1', 'p6'])

def add_to_class(student_email, class_id):
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                       {'$addToSet': {'students': student_email}})
    
def remove_from_class(student_email, class_id):
    classes = db['classes']
    classes.find_one_and_update({'_id' : ObjectId(class_id)},
                                {'$pull': {'students': student_email}})
    
def all_students_in_class(class_id):
    students = []
    emails = db['classes'].find_one({'_id': ObjectId(class_id)}).get('students')
    if emails == None:
        return {}
    for email in emails:
        students.append(db['students'].find_one({'student_email': email}))
    return students
