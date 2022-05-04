import sqlite3


def main(*args):
    # connection holds the connection to the database
    connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    # saving the values received by the client
    workflow_procedure_value = args[0]
    stations_value = args[1]

    # the databank operation that selects the workflow procedure value, matching the passed one
    c.execute("SELECT * FROM workflow_planner_table WHERE workflow_procedure = (?)",
              (workflow_procedure_value,))

    # saving the information from the database in items
    items = c.fetchall()

    # saving the stations from the database into a list called stations
    stations = items[0][1]
    stations = stations.split(";")

    # only a declaration of variables before the initialization
    item_pos = 0
    next_station = 00

    # iterating through all items inside stations
    for item in stations:
        # looking, which station in the database matches the station passed by the client
        if stations_value == item:
            print("Station gefunden! " + "\nPos: " + str(item_pos) + "\nStation: " + item)
            next_station = stations[item_pos + 1]
            print("Nächste Station: " + next_station)

    item_pos += 1

    # testprint
    print("Datenbankoperation ausgeführt!")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()

    return next_station
