import sqlite3


def next_in_queue(connection, cursor, procedure, station, next_station):
    c = cursor
    c.execute("SELECT MIN(production_number) FROM shop_info_table")
    production_number = c.fetchone()
    print("test " + str(production_number[0]))
    c.execute("SELECT * FROM shop_info_table WHERE production_number=(?)", (production_number[0],))
    entry = c.fetchone()
    print(entry)
    c.execute("INSERT INTO article_queue(order_id, article_id, station, next_station) VALUES (?, ?, ?, ?)", (entry[1], entry[2], station, next_station))
    connection.commit()

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
            # saving the next station
            next_station = stations[item_pos + 1]
            print("Nächste Station: " + next_station)

    item_pos += 1

    if workflow_procedure_value + " " + stations_value == \
            next_in_queue(connection, c, workflow_procedure_value, stations_value, next_station):
        pass

    print("Datenbankoperation ausgeführt, nächste Station übergeben.")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()

    # returning the next station
    return next_station

#######################TEST
# connection holds the connection to the database
connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

# cursor instance:
c = connection.cursor()

next_in_queue(connection, c, "001", "01", "02")
