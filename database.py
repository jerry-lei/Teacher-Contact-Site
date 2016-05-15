import sqlite3, hashlib

def makeTables():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    conn.commit()


