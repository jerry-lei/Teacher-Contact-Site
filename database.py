from pymongo import MongoClient
from datetime import datetime

connection = MongoClient()
db = connection['database']

def create_class(teacher_name, teacher_email, course_code, class_name, class_period):
    classes = db['classes']
    new_class = {'teacher_name': teacher_name,
                 'teacher_email': teacher_email,
                 'course_code': course_code,
                 'class_name': class_name,
                 'class_period': class_period}
    post_id = classes.insert_one(new_class).inserted_id
    return post_id

print create_class("Jerry Lei", "jlei2@stuy.edu", "E8SF-01", "Science Fiction", 3)
