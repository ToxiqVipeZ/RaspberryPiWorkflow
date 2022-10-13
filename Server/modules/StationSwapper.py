import sqlite3
import mysql.connector

DATABASE_PATH = "/Database/productionDatabase.db"
MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "production"


def next_in_queue(connection, cursor, procedure, station, next_station, variation_value):
    c = cursor
    c.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(%s)", (procedure,))
    article_id_queue = c.fetchone()
    article_id_queue = article_id_queue[0] + "-" + variation_value
    print("test: article_id_queue: " + article_id_queue)
    # queue position where procedure and station matches
    c.execute("SELECT MIN(queue_pos) FROM article_queue WHERE article_id=(%s) AND next_station=(%s)",
              (article_id_queue, station,))
    in_queue = cursor.fetchone()[0]
    queue_pos = in_queue
    print("(StationSwapper) queue pos: " + str(queue_pos))

    if station != next_station:
        if in_queue is None:
            in_queue = False

            # c.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(%s)", (procedure,))
            # article_id_queue = c.fetchone()
            # if article_id_queue != None:
            #    article_id_queue = article_id_queue[0]
            # regex = r"(" + re.escape(article_id_queue) + r")+[-]{1}[0-9]{2}"
            print("RFID nicht in der Warteschlange! " + article_id_queue + "\nVorgang: " +
                  procedure + "\nStation: " + station)

            c.execute(
                "SELECT MIN(production_number) FROM shop_info_table WHERE status_ident=(%s) AND article_id=(%s)",
                ("QUEUED", article_id_queue,))
            prod_nr = c.fetchone()[0]

            c.execute(
                "SELECT order_item_id, article_id FROM shop_info_table WHERE production_number=(%s)",
                (prod_nr,))
            fetch = c.fetchone()

            if article_id_queue == fetch[1]:
                article_id = fetch[1]
                order_item_id = fetch[0]
                print("artikelID: " + str(article_id) + "; order_item_id: "
                      + str(order_item_id) + "; prod_nr: " + str(prod_nr))

                c.execute(
                    "INSERT INTO article_queue(article_id, procedure, next_station) VALUES (%s, %s, %s)",
                    (article_id, procedure, next_station))
                connection.commit()

                c.execute(
                    "UPDATE shop_info_table SET status_ident=(%s) WHERE order_item_id=(%s) AND production_number=(%s)",
                    (next_station, order_item_id, prod_nr,))
                connection.commit()

        if in_queue:
            print("inqueueueueueueueueueueueue--------------------################--------------")

            c.execute("UPDATE article_queue SET next_station=(%s) WHERE queue_pos=(%s)",
                      (next_station, queue_pos,))
            connection.commit()
            print(str(station) + " + " + str(next_station) + " + " + str(queue_pos))

            if station == "01":
                station_status = "QUEUED"
            else:
                station_status = station

            c.execute(
                "SELECT MIN(production_number) FROM shop_info_table WHERE status_ident=(%s) AND article_id=(%s)",
                (station_status, article_id_queue,))
            prod_nr = c.fetchone()[0]

            # c.execute(
            #    "SELECT MIN(order_item_id) FROM shop_info_table WHERE article_id LIKE (%s) AND production_number=(%s)",
            #    (article_id, prod_nr,))
            # order_item_id = c.fetchone()[0]
            # print(order_item_id)

            c.execute(
                "UPDATE shop_info_table SET status_ident=(%s) WHERE production_number=(%s)",
                (next_station, prod_nr,))
            connection.commit()

    else:
        c.execute("UPDATE article_queue SET next_station=(%s) WHERE queue_pos=(%s)",
                  ("DONE", queue_pos,))
        connection.commit()

        c.execute(
            "SELECT MIN(production_number) FROM shop_info_table WHERE article_id LIKE (%s) AND status_ident=(%s)",
            (article_id_queue, station,))
        prod_nr = c.fetchone()[0]

        c.execute("UPDATE shop_info_table SET status_ident=(%s) WHERE production_number=(%s)", ("DONE", prod_nr,))
        connection.commit()


def main(*args):
    try:
        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        # saving the values received by the client
        workflow_procedure_value = args[0]
        stations_value = args[1]
        variation_value = args[2]

        # the databank operation that selects the workflow procedure value, matching the passed one
        c.execute("SELECT * FROM workflow_planner_table WHERE workflow_procedure = (%s)",
                  (workflow_procedure_value,))

        # saving the information from the database in items
        items = c.fetchall()

        # saving the stations from the database into a list called stations
        stations = items[0][1]
        stations = stations.split(";")

        # only a declaration of variables before the initialization
        iterator = 0

        # iterating through all items inside stations
        for item in stations:
            # looking, which station in the database matches the station passed by the client
            if stations_value == item:
                print("Station gefunden! " + "\nPos: " + str(iterator) + "\nStation: " + item)
                # saving the next station
                next_station = stations[iterator + 1]
                print("Nächste Station: " + next_station)
                next_in_queue(connection, c, workflow_procedure_value, stations_value, next_station, variation_value)
                break
            iterator += 1

        print("Datenbankoperation ausgeführt, nächste Station übergeben.")

        # committing the created table:
        connection.commit()

        # closing the connection
        connection.close()

        # returning the next station
        return next_station

    except IndexError:
        next_in_queue(connection, c, workflow_procedure_value, stations_value, stations_value, variation_value)
        return "no next station"

#######################TEST
# connection holds the connection to the database
# connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

# cursor instance:
# c = connection.cursor()

# next_in_queue(connection, c, "001", "01", "02")

# connection.close()
