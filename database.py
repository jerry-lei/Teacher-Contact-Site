from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from datetime import datetime

connection = MongoClient()
db = connection['database']


def create_class(teacher_name, teacher_email, course_code, class_name):
    classes = db['classes']
    new_class = {'teacher_name': teacher_name,
                 'teacher_email': teacher_email,
                 'course_code': course_code,
                 'class_name': class_name,}
    post_id = classes.insert_one(new_class).inserted_id
    return post_id

print create_class("Lei", "jlei2@stuy.edu", "E8SF-01", "Science Fiction")
