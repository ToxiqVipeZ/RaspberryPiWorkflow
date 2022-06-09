import sqlite3
import datetime

DATABASE_PATH = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"


class ServerHandler:

    def station_in(self, rfid, station):
        variant = rfid[5:]
        procedure = rfid[2:5]

        # connection holds the connection to the database
        connection = sqlite3.connect(DATABASE_PATH)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(?)", (procedure,))
        article_id = cursor.fetchone()[0]

        # adding the variant to the article_id
        article_id = article_id + "-" + variant

        cursor.execute("SELECT MIN(process_id) FROM process_time_table WHERE article_id=(?)", (article_id,))
        process_id = cursor.fetchone()[0]

        # getting production_number information
        cursor.execute("SELECT MIN(production_number) FROM shop_info_table WHERE article_id=(?)", (article_id,))
        prod_nr = cursor.fetchone()[0]

        cursor.execute("SELECT order_id FROM shop_info_table WHERE production_number=(?)", (prod_nr,))
        order_id = cursor.fetchone()[0]

        cursor.execute("SELECT stations FROM workflow_planner_table WHERE workflow_procedure=(?)", (procedure,))
        stations = cursor.fetchone()[0]
        print(stations)
        splitted_stations = stations.split[";"]
        last_station = splitted_stations[-1]
        counter = 0

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
                       "last_station, process_start) VALUES (?,?,?,?,?,?,?)",
                       (prod_nr, article_id, order_id, station, next_station, last_station, current_datetime))

        connection.commit()

        # Closing the connection
        connection.close()

    def station_out(self, rfid, station):
        variant = rfid[5:]
        procedure = rfid[2:5]

        # connection holds the connection to the database
        connection = sqlite3.connect(DATABASE_PATH)
        # cursor instance:
        cursor = connection.cursor()

        # getting article_id
        cursor.execute("SELECT article_id FROM article_procedure_table WHERE procedure=(?)", (procedure,))
        article_id = cursor.fetchone()[0]

        # adding the variant to the article_id
        article_id = article_id + "-" + variant

        cursor.execute("SELECT MIN(process_id) FROM process_time_table WHERE article_id=(?) AND "
                       "station=(?)", (article_id, station))
        process_id = cursor.fetchone()[0]

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        cursor.execute("UPDATE process_time_table SET process_end=(?) WHERE process_id=(?)",
                       (current_datetime, process_id,))

        connection.commit()

        connection.close()
