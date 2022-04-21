import sqlite3

# connection holds the connection to the database
connection = sqlite3.connect("productionDatabase.db")

# cursor instance:
c = connection.cursor()

c.execute("DROP TABLE lager")

# testprint
print("execute ausgeführt!")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
