import mysql.connector
import time

ADD_TO_QUEUE = "RFID-QUEUE-ADD"
STAT_ORDER_IN = "ORDER-IN"
STAT_QUEUED = "QUEUED"
# PRODUCTION_DATABASE = "/home/pi/ServerFiles/Database/ProductionDatabase.db"
# PRODUCTION_DATABASE = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"

MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "production"


def queue_order(connection, cursor, production_number):
    print(production_number)
    cursor.execute("SELECT order_id, article_id FROM shop_info_table WHERE production_number = (%s)",
                   (production_number,))
    fetch = cursor.fetchmany(2)
    print(fetch)
    order_id = (fetch[0][0])
    article_id = (fetch[0][1])
    print(order_id)
    print(article_id)

    cursor.execute("UPDATE shop_info_table SET status_ident=(%s) WHERE production_number LIKE (%s)",
                   (STAT_QUEUED, production_number,))
    connection.commit()


class DatabaseQueue:

    def __init__(self):
        self.main()

    @staticmethod
    def main():
        while True:
            try:
                # connection holds the connection to the database
                connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                                     passwd=MYSQL_PASSWD, db=MYSQL_DB)
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM shop_info_table")
                contents = cursor.fetchall()
                print(contents)

                if contents is not None:
                    cursor.execute("SELECT MIN(production_number) FROM shop_info_table WHERE status_ident = (%s)",
                                   (STAT_ORDER_IN, ))
                    list_not_empty = cursor.fetchone()[0]

                    production_number = list_not_empty

                    if list_not_empty is None:
                        list_not_empty = False

                    time.sleep(10)
                    print("\nWarte auf neue Bestellungen um sie der Warteschlange hinzuzufügen. (5s)\n")

                    if list_not_empty:
                        queue_order(connection, cursor, production_number)

                else:
                    time.sleep(10)
                    print("\nWarte auf neue Bestellungen um sie der Warteschlange hinzuzufügen. (5s)\n")


            except KeyboardInterrupt:
                print("Program exited on STRG-C")


if __name__ == "__main__":
    DatabaseQueue.main()
