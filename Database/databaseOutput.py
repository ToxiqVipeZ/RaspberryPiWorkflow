import sqlite3

# connection holds the connection to the database
connection = sqlite3.connect("productionDatabase.db")

# cursor instance:
c = connection.cursor()

c.execute("SELECT * FROM workflow_planner_table ORDER BY workflow_procedure")
items = c.fetchall()

for item in items:
    print(item)

# testprint
print("execute ausgeführt!")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
