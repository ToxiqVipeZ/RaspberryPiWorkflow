import sqlite3
from datetime import datetime


def main():
    # connection holds the connection to the database
    #connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")
    connection = sqlite3.connect("productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    # c.execute("INSERT INTO error_list_table (error_id, error_type, error_message) VALUES (?,?,?)",
    #           (2, "emotional damage"))
    c.execute("UPDATE process_time_table SET process_id=(?), station=(?), next_station=(?) WHERE process_id=(?)", (1, "01", "02", 10))



    #c.execute("DELETE FROM process_time_table WHERE process_id=(?)",(12,))

    #time_now = "21.07.2022 10:42:30"
    #process_id = 9

    #c.execute("UPDATE process_time_table SET process_start=(?) WHERE process_id=(?)", (time_now, process_id))

    #c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
    #          " next_station, last_station, process_start) VALUES "
    #          "(?, ?, ?, ?, ?, ?, ?)",
    #          (12, "0010013-05", 3, "04", "05", "05", "21.07.2022 08:55:00"))

    #c.execute("UPDATE process_time_table SET process_end=(?) WHERE process_id=(?)", (time_now,process_id ))

    # c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
    #          " next_station, last_station, process_start, process_end) VALUES "
    #          "(?, ?, ?, ?, ?, ?, ?, ?)",
    #          (7, "0010013-01", 2, "02", "05", "05", "13.07.2022 15:11:00", "13.07.2022 15:13:00"))

    # c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
    #          " next_station, last_station, process_start) VALUES "
    #          "(?, ?, ?, ?, ?, ?, ?)",
    #          (10, "0010013-01", 11, "03", "04", "05", "08.07.2022 10:52:00"))

    # c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
    #          " next_station, last_station, process_start) VALUES "
    #          "(?, ?, ?, ?, ?, ?, ?)",
    #          (10, "0010013-01", 11, "03", "04", "05", "08.07.2022 10:52:00"))

    # c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
    #          " next_station, last_station, process_start) VALUES "
    #          "(?, ?, ?, ?, ?, ?, ?)",
    #          (10, "0010013-01", 11, "03", "04", "05", "08.07.2022 10:52:00"))

    """
    
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start, process_end) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?)",
              (1, "0010012-01", 1, "01", "02", "05", "28.06.2022 01:00:00", "28.06.2022 01:05:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start, process_end) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?)",
              (2, "0010012-01", 1, "02", "05", "05", "28.06.2022 01:06:00", "28.06.2022 01:10:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start, process_end) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?)",
              (3, "0010012-01", 1, "05", "Kunde", "05", "28.06.2022 01:11:00", "28.06.2022 01:15:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start, process_end) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?)",
              (4, "0010012-01", 1, "01", "02", "05", "28.06.2022 01:16:00", "28.06.2022 01:20:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start) VALUES "
              "(?, ?, ?, ?, ?, ?, ?)",
              (5, "0010012-01", 1, "01", "02", "05", "28.06.2022 01:21:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start, process_end) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?)",
              (6, "0010012-01", 2, "01", "02", "05", "28.06.2022 01:06:00", "28.06.2022 01:10:00"))
    
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start) VALUES "
              "(?, ?, ?, ?, ?, ?, ?)",
              (8, "0010012-01", 2, "05", "Kunde", "05", "28.06.2022 01:16:00"))
    c.execute("INSERT INTO process_time_table (process_id, article_id, order_id, station,"
              " next_station, last_station, process_start) VALUES "
              "(?, ?, ?, ?, ?, ?, ?)",
              (9, "0010012-01", 2, "02", "05", "05", "28.06.2022 01:16:00"))
"""

    # c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE status_ident IS NULL", ("ORDER-IN", ))
    # c.execute("SELECT status_ident FROM shop_info_table WHERE production_number=(?)", ("1"))
    # print(c.fetchone())

    # testprint
    print("execute ausgeführt!")

    # committing the created table:
    connection.commit()

    # closing the connection
    connection.close()


main()

"""
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (1, "0010012-01", 101, "02", "05", "05", "21.06.2022 09:11:00", "21.06.2022 09:15:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (2, "0010012-01", 101, "01", "02", "05", "21.06.2022 09:14:00", "21.06.2022 09:20:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (2, "0010012-01", 101, "02", "05", "05", "21.06.2022 09:21:00", "21.06.2022 09:25:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (1, "0010012-01", 101, "05", "Kunde", "05", "21.06.2022 09:17:00", "21.06.2022 09:23:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (2, "0010012-01", 101, "05", "Kunde", "05", "21.06.2022 09:26:00", "21.06.2022 09:28:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (3, "0010012-01", 102, "01", "02", "05", "21.06.2022 09:21:00", "21.06.2022 09:27:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (4, "0010012-01", 103, "01", "02", "05", "21.06.2022 09:28:00", "21.06.2022 09:31:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (5, "0010012-01", 104, "01", "02", "05", "21.06.2022 09:32:00", "21.06.2022 09:39:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (3, "0010012-01", 102, "02", "05", "05", "21.06.2022 09:28:00", "21.06.2022 09:34:00"))
    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (3, "0010012-01", 102, "05", "Kunde", "05", "21.06.2022 09:35:00", "21.06.2022 09:39:00"))
"""
