# Выбор элементов и функции в SQL запросах

import sqlite3

file = open('not_telegram.db', 'w')
file.close()

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")

# Заполните её 10 записями
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i * 10, 1000))

# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
for i in range(1, 11, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, f"User{i}",))

# Удалите каждую 3ую запись в таблице начиная с 1ой:
for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))

# Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
# for user in users:
#     print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")

# Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

# Подсчитать общее количество записей.
cursor.execute("SELECT COUNT (*) FROM Users")
count_users = cursor.fetchone()[0]

# Посчитать сумму всех балансов.
cursor.execute("SELECT SUM(balance) FROM Users")
summ_balance = cursor.fetchone()[0]

# Вывести в консоль средний баланс всех пользователя.
print(summ_balance / count_users)

# cursor.execute("SELECT AVG(balance) FROM Users")
# avg_balance = cursor.fetchone()[0]
# print(avg_balance)

connection.commit()
connection.close()
