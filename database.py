from pymongo import MongoClient
from datetime import datetime

connection = MongoClient()
db = connection['database']

def create_student(student_name, student_email):
    pass

def create_teacher(teacher_name, teacher_email):
    pass

def create_class(teacher_name, teacher_email, course_code, class_name, class_period):
    classes = db['classes']
    new_class = {'teacher_name': teacher_name,
                 'teacher_email': teacher_email,
                 'course_code': course_code,
                 'class_name': class_name,
                 'class_period': class_period}
    classes.insert_one(new_class)
