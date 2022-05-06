import sqlite3
import time

ADD_TO_QUEUE = "RFID-QUEUE-ADD"
STAT_ORDER_IN = "ORDER-IN"
STAT_QUEUED = "QUEUED"


def queue_order(connection, cursor, production_number):
    print(production_number)
    cursor.execute("SELECT order_id, article_id FROM shop_info_table WHERE production_number IS (?)",
                        (production_number,))
    fetch = cursor.fetchmany(2)
    print(fetch)
    order_id = (fetch[0][0])
    article_id = (fetch[0][1])
    print(order_id)
    print(article_id)

    cursor.execute("UPDATE shop_info_table SET status_ident=(?) WHERE production_number LIKE (?)",
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
                connection = sqlite3.connect(
                    "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")
                cursor = connection.cursor()

                cursor.execute("SELECT MIN(production_number) FROM shop_info_table WHERE status_ident IS NOT (?)",
                               (STAT_QUEUED,))
                list_not_empty = cursor.fetchone()[0]

                production_number = list_not_empty

                if list_not_empty is None:
                    list_not_empty = False

                time.sleep(5)
                print("\nWarte auf neue Bestellungen um sie der Warteschlange hinzuzufügen. (5s)\n")

                if list_not_empty:
                    queue_order(connection, cursor, production_number)


            except KeyboardInterrupt:
                print("Program exited on STRG-C")

if __name__ == "__main__":
    DatabaseQueue.main()
