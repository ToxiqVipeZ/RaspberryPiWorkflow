import sqlite3


# connection holds the connection to the database
connection = sqlite3.connect("productionDatabase.db")

# cursor instance:
c = connection.cursor()

# drop table:
c.execute("DROP TABLE process_time_table")

# creating a table:
c.execute("""
CREATE TABLE process_time_table (
process_id INTEGER PRIMARY KEY,
article_id INTEGER NOT NULL,
station INTEGER,
last_station INTEGER,
process_start TEXT,
process_time TEXT
)""")

# drop table:
c.execute("DROP TABLE workflow_planner_table")

# creating a table:
c.execute("""
CREATE TABLE workflow_planner_table (
workflow_procedure TEXT UNIQUE,
stations TEXT
)""")

# drop table:
#c.execute("DROP TABLE shop_info_table")

# creating a table:
#c.execute("""
#CREATE TABLE shop_info_table (
#order_item_id INTEGER,
#order_id INTEGER,
#article_id TEXT,
#status_ident TEXT,
#TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
#production_number INTEGER PRIMARY KEY
#)""")

# drop table:
c.execute("DROP TABLE article_procedure_table")

# creating a table:
c.execute("""
CREATE TABLE article_procedure_table (
article_id TEXT UNIQUE,
procedure TEXT UNIQUE
)""")

c.execute("DROP TABLE article_queue")

c.execute("""
CREATE TABLE article_queue (
queue_pos INTEGER PRIMARY KEY,
order_id INTEGER,
article_id TEXT,
station TEXT,
next_station TEXT
)""")

# committing the created table:
connection.commit()

# closing the connection
connection.close()
