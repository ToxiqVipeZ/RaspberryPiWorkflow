import sqlite3


def main(*args):
    # connection holds the connection to the database
    connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE status_ident IS NULL", ("ORDER-IN", ))
    c.execute("SELECT status_ident FROM shop_info_table WHERE production_number=(?)", ("1"))
    print(c.fetchone())

    # c.execute("INSERT INTO workflow_planner_table VALUES (?, ?)", (workflow_procedure_value, stations_value))

    # testprint
    print("execute ausgeführt!")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()

main()