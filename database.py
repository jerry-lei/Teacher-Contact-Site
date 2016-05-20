from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from datetime import datetime

connection = MongoClient()
db = connection['database']

