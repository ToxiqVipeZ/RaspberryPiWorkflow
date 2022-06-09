import sqlite3

DATABASE_PATH = "/Database/productionDatabase.db"

class ServerHandler:

    def station_in(self):
        # connection holds the connection to the database
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        cursor = connection.cursor()

        cursor.execute("INSERT INTO process_time_table VALUES (?,?,?,?,?,?)")

        connection.close()

    def station_out(self):
        # connection holds the connection to the database
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        cursor = connection.cursor()

        connection.close()
