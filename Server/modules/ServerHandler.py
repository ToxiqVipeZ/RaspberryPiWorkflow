import sqlite3
import mysql.connector
import datetime

# DATABASE_PATH = "/Database/productionDatabase.db"
DATABASE_PATH = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "wordpress"


class ServerHandler:

    def station_in(self, rfid, station):
        print("ServerHandler called! station = " + station)
        variant = rfid[5:]
        procedure = rfid[2:5]

        if station == "01":
            station = "QUEUED"

        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(%s)", (procedure,))
        article_id = cursor.fetchone()[0]

        # adding the variant to the article_id
        article_id = article_id + "-" + variant

        print("ServerHandler articleID: " + article_id)
        # cursor.execute("SELECT MIN(process_id) FROM process_time_table WHERE article_id=(%s)", (article_id,))
        # process_id = cursor.fetchone()[0]

        # getting production_number information
        cursor.execute("SELECT production_number FROM shop_info_table WHERE article_id=(%s) AND status_ident=(%s)",
                       (article_id, station,))
        prod_nr = cursor.fetchone()[0]
        print("Server_handler prod_nr: " + str(prod_nr))

        cursor.execute("SELECT MIN(order_id) FROM shop_info_table WHERE production_number=(%s)", (prod_nr,))
        order_id = cursor.fetchone()[0]
        print("Server_handler order_id: " + str(order_id))

        cursor.execute("SELECT MIN(stations) FROM workflow_planner_table WHERE workflow_procedure=(%s)", (procedure,))
        stations = cursor.fetchone()[0]
        print(stations)
        splitted_stations = stations.split(";")
        last_station = splitted_stations[-1]
        counter = 0

        if station == "QUEUED":
            station = "01"

        if station == last_station:
            next_station = "Kunde"
        else:
            for x in splitted_stations:
                if x == station:
                    next_station = splitted_stations[counter + 1]
                    break
                counter += 1

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        cursor.execute("INSERT INTO process_time_table(process_id, article_id, order_id, station, next_station,"
                       "last_station, process_start) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (prod_nr, article_id, order_id, station, next_station, last_station, current_datetime))

        connection.commit()

        # Closing the connection
        connection.close()

    def station_out(self, rfid, station):
        print("ServerHandler called! station = " + station)
        variant = rfid[5:]
        procedure = rfid[2:5]

        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(%s)", (procedure,))
        article_id = cursor.fetchone()[0]

        # adding the variant to the article_id
        article_id = article_id + "-" + variant

        print("ServerHandler articleID: " + article_id)

        cursor.execute("SELECT MIN(process_id) FROM process_time_table WHERE article_id=(%s) AND "
                       "station=(%s)", (article_id, station,))
        process_id = cursor.fetchone()[0]

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        cursor.execute("UPDATE process_time_table SET process_end=(%s) WHERE process_id=(%s)",
                       (current_datetime, process_id,))

        connection.commit()

        connection.close()

    def error_in(self, error, error_message):
        error = error.split(", ")
        error_id = error[0]
        error_type = error[1]

        error_message = error_message.split("SplitStatement15121 ")
        station_nr = error_message[1]
        error_message = error_message[0]

        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # getting article_id
        cursor.execute("INSERT INTO error_history_table (error_id, error_type, error_message, station_nr, "
                       "error_start, error_end, error_duration) "
                       "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (error_id, error_type, error_message, station_nr, current_datetime, "waiting", "waiting"))

        connection.commit()

        connection.close()

    def error_out(self, error, error_message):
        error = error.split(", ")
        error_id = error[0]
        error_type = error[1]

        error_message = error_message.split("SplitStatement15121 ")
        station_nr = error_message[1]
        error_message = error_message[0]

        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        cursor.execute("SELECT error_start FROM error_history_table "
                       "WHERE error_id=(%s) AND station_nr=(%s) AND error_end=(%s) and error_duration=(%s)",
                       (error_id, station_nr, "waiting", "waiting"))
        error_start = cursor.fetchone()[0]

        time_check_in = datetime.datetime.strptime(error_start, "%d.%m.%Y %H:%M:%S")
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        time_now = datetime.datetime.strptime(current_datetime, "%d.%m.%Y %H:%M:%S")
        difference = time_now - time_check_in

        # getting article_id
        cursor.execute("UPDATE error_history_table "
                       "SET error_end=(%s), error_duration=(%s) "
                       "WHERE error_id=(%s) AND station_nr=(%s)",
                       (str(current_datetime), str(difference), error_id, station_nr))

        connection.commit()

        connection.close()

    def error_resolved(self):
        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT * FROM error_list_table")
        error_list = cursor.fetchall()

        connection.commit()

        connection.close()

    def get_error_list(self):
        # connection holds the connection to the database
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                             passwd=MYSQL_PASSWD, db=MYSQL_DB)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT * FROM error_list_table")
        error_list = cursor.fetchall()

        connection.commit()

        connection.close()

        return error_list
