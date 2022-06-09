import sqlite3


def main():
    # connection holds the connection to the database
    connection = sqlite3.connect("productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    # process-time-table
    #ptt_reset(connection, c)
    # workflow-planner-table
    #wpt_reset(connection, c)
    # article-procedure-table
    #apt_reset(connection, c)
    # shop-info-table
    #sit_reset(connection, c)
    # article-queue
    #aq_reset(connection, c)

    # closing the connection
    connection.close()

def ptt_reset(connection, c):
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
    process_end TEXT
    )""")

    # committing the created table:
    connection.commit()


def wpt_reset(connection, c):
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


def sit_reset(connection, c):
    # drop table:
    c.execute("DROP TABLE shop_info_table")

    # creating a table:
    c.execute("""
    CREATE TABLE shop_info_table (
    order_item_id INTEGER,
    order_id INTEGER,
    article_id TEXT,
    status_ident TEXT,
    time_stamp TEXT,
    production_number INTEGER PRIMARY KEY
    )""")

    # committing the created table:
    connection.commit()


def apt_reset(connection, c):
    # drop table:
    c.execute("DROP TABLE article_procedure_table")

    # creating a table:
    c.execute("""
    CREATE TABLE article_procedure_table (
    article_id TEXT UNIQUE,
    procedure TEXT UNIQUE
    )""")

    # committing the created table:
    connection.commit()


def aq_reset(connection, c):
    c.execute("DROP TABLE article_queue")

    c.execute("""
    CREATE TABLE article_queue (
    queue_pos INTEGER PRIMARY KEY,
    article_id TEXT,
    procedure TEXT,
    next_station TEXT
    )""")

    # committing the created table:
    connection.commit()


if __name__ == '__main__':
    main()
