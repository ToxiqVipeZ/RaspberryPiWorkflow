import sqlite3
import re


def next_in_queue(connection, cursor, procedure, station, next_station):
    c = cursor
    # queue position where procedure and station matches
    c.execute("SELECT MIN(queue_pos) FROM article_queue WHERE procedure=(?) AND next_station=(?)",
              (procedure, station,))
    in_queue = cursor.fetchone()[0]
    queue_pos = in_queue
    print("test " + str(queue_pos))

    if station != next_station:

        if in_queue is None:
            in_queue = False

            c.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(?)", (procedure,))
            article_id_queue = c.fetchone()[0]
            regex = r"(" + re.escape(article_id_queue) + r")+[-]{1}[0-9]{2}"
            print("RFID nicht in der Warteschlange! " + article_id_queue + ": " + procedure + "; " + station)

            c.execute(
                "SELECT order_item_id, article_id FROM shop_info_table WHERE status_ident=(?) ORDER BY order_item_id",
                ("QUEUED",))
            fetch = c.fetchall()
            for item in fetch:
                if re.match(regex, item[1]):
                    article_id = item[1]
                    order_item_id = item[0]
                    print("artikelID: " + str(article_id) + "; order_item_id: " + str(order_item_id))

                    c.execute(
                        "INSERT INTO article_queue(article_id, procedure, next_station) VALUES (?, ?, ?)",
                        (article_id, procedure, next_station))
                    connection.commit()

                    c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE order_item_id=(?)",
                              (next_station, order_item_id,))
                    connection.commit()

                    break

        if in_queue:
            print("inqueueueueueueueueueueueue-----------------------------------------------------------------")
            c.execute("UPDATE article_queue SET next_station=(?) WHERE queue_pos=(?)",
                      (next_station, queue_pos,))
            connection.commit()
            print(str(station) + " + " + str(next_station) + " + " + str(queue_pos))
            c.execute("SELECT article_id FROM article_queue WHERE queue_pos=(?)",
                      (queue_pos,))
            article_id = c.fetchone()[0]
            print(article_id)
            c.execute(
                "SELECT MIN(order_item_id) FROM shop_info_table WHERE article_id LIKE (?) AND status_ident=(?)",
                (article_id, station,))
            order_item_id = c.fetchone()[0]
            print(order_item_id)
            c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE order_item_id=(?)", (next_station, order_item_id,))
            connection.commit()

    else:
        c.execute("UPDATE article_queue SET next_station=(?) WHERE queue_pos=(?)",
                  ("DONE", queue_pos,))
        connection.commit()

        c.execute("SELECT article_id FROM article_queue WHERE queue_pos=(?)",
                  (queue_pos,))
        article_id = c.fetchone()[0]

        c.execute(
            "SELECT MIN(order_item_id) FROM shop_info_table WHERE article_id LIKE (?) AND status_ident=(?)",
            (article_id, station,))
        order_item_id = c.fetchone()[0]

        c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE order_item_id=(?)", ("DONE", order_item_id,))
        connection.commit()


def main(*args):
    try:
        # connection holds the connection to the database
        connection = sqlite3.connect(
            "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

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
        # item_pos = 0
        # next_station = 00
        iterator = 0

        # iterating through all items inside stations
        for item in stations:
            # looking, which station in the database matches the station passed by the client
            if stations_value == item:
                print("Station gefunden! " + "\nPos: " + str(iterator) + "\nStation: " + item)
                # saving the next station
                next_station = stations[iterator + 1]
                print("Nächste Station: " + next_station)
                next_in_queue(connection, c, workflow_procedure_value, stations_value, next_station)
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
        next_in_queue(connection, c, workflow_procedure_value, stations_value, stations_value)
        return "no next station"

#######################TEST
# connection holds the connection to the database
# connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

# cursor instance:
# c = connection.cursor()

# next_in_queue(connection, c, "001", "01", "02")

# connection.close()
