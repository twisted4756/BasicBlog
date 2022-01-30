import sqlite3


conection = sqlite3.connect("users.db")
cursor = conection.cursor()

cursor.execute("""CREATE TABLE user (
                user text,
                password text
                )""")

conection.commit()

conection.close()