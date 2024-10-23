import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def initiate_db():
    file = open('database.db', 'w')
    file.close()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY, 
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        pict TEXT)
        """)
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS Users(
       id INTEGER PRIMARY KEY, 
       username  TEXT NOT NULL,
       email TEXT NOT NULL,
       age  INTEGER NOT NULL,
       balance INTEGER NOT NULL)
       """)
    connection.commit()
    # connection.close()


def add_product(id_, title_, description_, price_, pict_):
    cursor.execute(f"INSERT INTO Products (title,description,price,pict) VALUES (?, ?, ?, ?)",
                   (title_, description_, price_, pict_))
    connection.commit()
    # connection.close()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    return products


def is_included(username):
    cursor.execute(f"SELECT * FROM Users WHERE username= '{username}'")
    if cursor.fetchone() is None:
        return False
    else:
        return True


def add_user(username, email, age):
    cursor.execute(f"INSERT INTO Users (username,email,age,balance) VALUES(?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()


if __name__ == "__main__":
    initiate_db()
    for i in range(1, 5):
        add_product(f"{i}", f"Продукт {i}", f"Описание {i}", f"{100 * i}", f"BAD_{i}.webp")
    add_user('User1', 'user1@mail.ru', 30)
    connection.close()
