# Python Code to query the database “data.db” to fetch the records
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('SELECT * FROM person')
print(c.fetchall())
c.execute('SELECT * FROM address')
print(c.fetchall())
conn.close()
