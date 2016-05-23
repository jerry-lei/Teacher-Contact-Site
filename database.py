from pymongo import MongoClient
from datetime import datetime

connection = MongoClient()
db = connection['database']

def create_student(student_name, student_email):
    students = db['students']
    print students.find_one({'student_email': student_email})
    if students.find_one({'student_email': student_email}) == None:
        new_student = {'student_name': student_name,
                       'student_email': student_email,}
        students.insert_one(new_student)

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
                 'class_period': class_period}
    classes.insert_one(new_class)
