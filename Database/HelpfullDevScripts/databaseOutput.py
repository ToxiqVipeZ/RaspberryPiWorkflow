import datetime
import mysql.connector

MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "production"

# cursor instance:
connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                     passwd=MYSQL_PASSWD, db=MYSQL_DB)

c = connection.cursor()

print("")
print("Workflow Planer Tabelle: ")

c.execute("SELECT * FROM workflow_planner_table ORDER BY workflow_procedure")
items = c.fetchall()

for item in items:
    print(item)

print("\n\nArtikel <--> Vorgang - Relationstabelle: ")

c.execute("SELECT * FROM article_procedure_table ORDER BY procedure_id")
items = c.fetchall()

for item in items:
    print(item)


print("\n\nshop info tabelle: ")

c.execute("SELECT * FROM shop_info_table ORDER BY order_id")
items = c.fetchall()

for item in items:
    print(item)

print("\n\narticle queue: ")

c.execute("SELECT * FROM article_queue ORDER BY queue_pos")
items = c.fetchall()

for item in items:
    print(item)


print("\n\nprocess_time_table: ")

c.execute("SELECT * FROM process_time_table ORDER BY process_id")
items = c.fetchall()

for item in items:
    print(item)

print("\n\nerror_list_table: ")

c.execute("SELECT * FROM error_list_table")
items = c.fetchall()

for item in items:
    print(item)

print("\n\nerror_history_table: ")

c.execute("SELECT * FROM error_history_table")
items = c.fetchall()

for item in items:
    print(item)

print("\n\narticle_parts_relation_table: ")

c.execute("SELECT * FROM article_parts_relation_table")
items = c.fetchall()

for item in items:
    print(item)

print("\n\ncassette_management_table: ")
c.execute("SELECT * FROM cassette_management_table")
items = c.fetchall()

for item in items:
    print(item)

print("\n\npart_storages_table: ")
c.execute("SELECT * FROM part_storages_table")
items = c.fetchall()

for item in items:
    print(item)

current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

print("\n" + current_datetime)
print("\n \nEnde des Outputs!")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
