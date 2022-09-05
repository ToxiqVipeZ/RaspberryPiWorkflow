import sqlite3


def main():
    # connection holds the connection to the database
    connection = sqlite3.connect("productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    # part-storages-table
    pst_reset(connection, c)

    # cassette-management-table
    #cmt_reset(connection, c)

    # article-parts-relation-list
    #aprt_reset(connection, c)

    # error-list-table
    #elt_reset(connection, c)

    # error-history-table
    #eht_reset(connection, c)

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

def pst_reset(connection, c):
    c.execute("DROP TABLE part_storages_table")

    c.execute(
        """
        CREATE TABLE part_storages_table (
        part_id TEXT PRIMARY KEY,
        part_amount INTEGER,
        in_cassettes BOOL
        )
        """
    )
    # committing the created table:
    connection.commit()

def cmt_reset(connection, c):
    c.execute("DROP TABLE cassette_management_table")

    c.execute(
        """
        CREATE TABLE cassette_management_table (
        cassette_id INTEGER PRIMARY KEY,
        cassette_contains TEXT,
        contains_amount INTEGER
        )
        """
    )
    # committing the created table:
    connection.commit()

def aprt_reset(connection, c):
    c.execute("DROP TABLE article_parts_relation_table")

    c.execute(
        """
        CREATE TABLE article_parts_relation_table (
        article_id TEXT PRIMARY KEY,
        part_id_list TEXT,
        part_id_list_amounts TEXT
        )
        """
    )
    # committing the created table:
    connection.commit()

def elt_reset(connection, c):
    # drop table:
    c.execute("DROP TABLE error_list_table")

    #create table:
    c.execute(
    """
    CREATE TABLE error_list_table (
    error_id INTEGER PRIMARY KEY,
    error_type TEXT NOT NULL
    )
    """
    )
    c.execute("INSERT INTO error_list_table (error_id, error_type) VALUES (?,?)",
              (1, "Maschinenversagen"))

    c.execute("INSERT INTO error_list_table (error_id, error_type) VALUES (?,?)",
              (2, "emotional damage"))

    c.execute("INSERT INTO error_list_table (error_id, error_type) VALUES (?,?)",
              (3, "Softwarefehler"))

    c.execute("INSERT INTO error_list_table (error_id, error_type) VALUES (?,?)",
              (9999, "Sonstige Fehler"))

    # committing the created table:
    connection.commit()


def eht_reset(connection, c):
    c.execute("DROP TABLE error_history_table")

    c.execute("""
        CREATE TABLE error_history_table (
        entry_id INTEGER PRIMARY KEY,
        error_id INTEGER NOT NULL,
        error_type TEXT NOT NULL,
        error_message TEXT,
        station_nr TEXT NOT NULL,
        error_start TEXT NOT NULL,
        error_end TEXT,
        error_duration TEXT
        )""")

    # committing the created table:
    connection.commit()

def ptt_reset(connection, c):
    # drop table:
    c.execute("DROP TABLE process_time_table")

    # creating a table:
    c.execute("""
    CREATE TABLE process_time_table (
    process_id INTEGER,
    article_id TEXT NOT NULL,
    order_id INTEGER NOT NULL,
    station TEXT NOT NULL,
    next_station TEXT NOT NULL,
    last_station TEXT NOT NULL,
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
    stations TEXT,
    times TEXT UNIQUE
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
