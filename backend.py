import sqlite3

def connect():
    conn=sqlite3.connect("appointment.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS appointment (id INTEGER PRIMARY KEY, uni text, doctor text, name text, email text, age integer,gender text, phone integer, address text)")
    conn.commit()
    conn.close()

def insert(uni,doctor,name,email,age,gender,phone,address):
    conn=sqlite3.connect("appointment.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO appointment VALUES (NULL,?,?,?,?,?,?,?,?)",(uni,doctor,name,email,age,gender,phone,address))
    conn.commit()
    conn.close()

connect()