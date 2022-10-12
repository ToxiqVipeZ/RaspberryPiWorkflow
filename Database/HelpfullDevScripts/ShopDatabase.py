#!/usr/bin/env python3
import mysql.connector
import sqlite3
import sys


def main():
    try:
        # connection holds the connection to the database
        #connection_prod_db = sqlite3.connect("productionDatabase.db")
        connection_shop_db = mysql.connector.connect(host="169.254.0.3", user="pi", passwd="raspberry", db="wordpress")
        DATABASE_PATH = "/home/pi/ServerFiles/Database/productionDatabase.db"
        # cursor instances:
        #c_prod_db = connection_prod_db.cursor()
        c_shop_db = connection_shop_db.cursor()

        #c_prod_db.execute("SELECT * FROM workflow_planner_table ORDER BY workflow_procedure")
        #items = c_prod_db.fetchall()

        c_shop_db.execute("SELECT * FROM Bestellergebnis")

        items = c_shop_db.fetchall()

        for item in items:
            print(item)

        # testprint
        print("execute ausgeführt!")

        # committing the created table:
        connection_shop_db.commit()

        # closing the connection
        connection_shop_db.close()

    except:
        print("exception thrown!\n" + sys.exc_info())


main()
