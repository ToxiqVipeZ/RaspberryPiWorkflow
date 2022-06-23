import sqlite3


def main():
    # connection holds the connection to the database
    connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

    # cursor instance:
    c = connection.cursor()

    c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (9, "test", 105, "01", "02", "05", "25.06.2022 7:22:00", "25.06.2022 7:27:00"))

    #c.execute("UPDATE shop_info_table SET status_ident=(?) WHERE status_ident IS NULL", ("ORDER-IN", ))
    #c.execute("SELECT status_ident FROM shop_info_table WHERE production_number=(?)", ("1"))
    #print(c.fetchone())


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