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

# committing the created table:
connection.commit()

# closing the connection
connection.close()
