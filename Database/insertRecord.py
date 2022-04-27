import sqlite3


def main(*args):
    # connection holds the connection to the database
    connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    workflow_procedure_value = args[0]
    stations_value = args[1]

    print(workflow_procedure_value)
    print(stations_value)

    c.execute("INSERT INTO workflow_planner_table VALUES (?, ?)", (workflow_procedure_value, stations_value))

    # testprint
    print("execute ausgeführt!")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()
