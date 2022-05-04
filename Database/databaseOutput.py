import sqlite3

# connection holds the connection to the database
connection = sqlite3.connect("productionDatabase.db")

# cursor instance:
c = connection.cursor()
print("")
print("Workflow Planer Tabelle: ")

c.execute("SELECT * FROM workflow_planner_table ORDER BY workflow_procedure")
items = c.fetchall()

for item in items:
    print(item)

print("\n\nArtikel <--> Vorgang - Relationstabelle: ")

c.execute("SELECT * FROM article_procedure_table ORDER BY procedure")
items = c.fetchall()

for item in items:
    print(item)


print("\n\nshop info tabelle: ")

c.execute("SELECT * FROM shop_info_table ORDER BY order_id")
items = c.fetchall()

for item in items:
    print(item)


print("\n \nEnde des Outputs!")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
