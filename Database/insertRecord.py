import sqlite3

process_id =
process_step = 1

# connection holds the connection to the database
connection = sqlite3.connect("productionDatabase.db")

# cursor instance:
c = connection.cursor()

if process_step != 0:


c.execute("INSERT INTO process_time_table VALUES (NULL, 0, 0, 0, datetime(), time())")

# testprint
print("execute ausgeführt!")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
