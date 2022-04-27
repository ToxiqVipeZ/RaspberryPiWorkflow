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

    c.execute("SELECT * FROM workflow_planner_table WHERE workflow_procedure = (?)",
              (workflow_procedure_value,))

    items = c.fetchall()
    stations = items[0][1]
    stations = stations.split(";")
    item_pos = 0
    next_station = 00

    for item in stations:

        if stations_value == item:
            print("Station gefunden! " + str(item_pos) + " " + item)
            next_station = stations[item_pos + 1]
            print(next_station)

    item_pos += 1

    # testprint
    print("execute ausgeführt!")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()

    return next_station
