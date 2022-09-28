#!/usr/bin/env python3
import sqlite3
import mysql.connector
import time
import datetime

STATUS = "ORDER-IN"
MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "wordpress"
#SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
SQLITE3_HOST = "/home/pi/ServerFiles/Database/productionDatabase.db"


class ShopInformationCollector:
    connection_closed = False

    def main(self):
        # Database-connection
        print("Baue Shop-Datenbankverbindung auf....")
        connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        print("Baue Produktions-Datenbankverbindung auf....")
        production_connection = sqlite3.connect(
            SQLITE3_HOST)
        print("Datenbankverbindung steht!")
        cursor = connection.cursor()
        prod_cursor = production_connection.cursor()
        try:
            # main loop
            while True:

                cursor.execute(
                    "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
                shop_oid_max_read = cursor.fetchone()
                shop_oid_max = shop_oid_max_read[0]

                cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
                cor_oid_max_read = cursor.fetchone()
                cor_oid_max = cor_oid_max_read[0]

                # Wenn die neuste Bestellung (shop_oid_max) bereits im custom_order_receiver(cor_oid_max) ist:
                # Bedeutet, es gibt keine neue Bestellung, welche noch nicht aufgenommen wurde
# som == com
                if shop_oid_max == cor_oid_max:
                    while shop_oid_max == cor_oid_max:
                        #self.som_com_request(cursor, prod_cursor)
                        cursor.execute(
                            "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
                        shop_oid_max_read = cursor.fetchone()
                        shop_oid_max = shop_oid_max_read[0]
                        connection.commit()

                        cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
                        cor_oid_max_read = cursor.fetchone()
                        cor_oid_max = cor_oid_max_read[0]
                        production_connection.commit()

                        print("Warte 5s auf Bestelleingangsscan")
                        time.sleep(5)

# som > com
                # if the shop has a new Order:
                if shop_oid_max > cor_oid_max:
                    while shop_oid_max > cor_oid_max:

                        # get the newest order_id
                        cursor.execute(
                            "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
                        resmaxorder = cursor.fetchone()
                        for maxo in resmaxorder:
                            print("wp-wo-oi: Max Order ID: " + str(maxo))
                            read_order_id = maxo

                            # get order_item_id for the acquired order_id
                            cursor.execute(
                                "SELECT order_item_ID FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%') AND order_id=%s",
                                (read_order_id,))
                            order_item_id_fetch = cursor.fetchall()
                            for data1 in order_item_id_fetch:
                                read_order_item_id = str(data1[0])
                                print("wp-wo-oi: Max Order Item ID: " + str(read_order_item_id))

                                # get the amount of items ordered with the acquired order_item_id
                                cursor.execute(
                                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
                                    (read_order_item_id,))
                                amount = cursor.fetchone()
                                amount = amount[0]
                                qty = int(amount)

                                # if the ordered amount is greater one
                                if qty > 1:
                                    while qty > 1:

                                        # get the system-given variation id:
                                        cursor.execute(
                                            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                                            (read_order_item_id,))
                                        variation = cursor.fetchall()
                                        for data3 in variation:
                                            variation = str(data3[0])
                                            print("wp-wo-oimeta: Variation: " + variation)

                                            # use the system-given variation id to find related article-id's
                                            cursor.execute(
                                                "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                                                (variation,))
                                            article_id = cursor.fetchone()

                                            current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                                            cursor.execute(
                                                "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident, time_stamp)"
                                                " VALUES (%s, %s, %s, %s, %s)",
                                                (read_order_item_id, read_order_id, article_id[0], STATUS, current_datetime))
                                            connection.commit()

                                            prod_cursor.execute(
                                                "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident, time_stamp)"
                                                " VALUES (?, ?, ?, ?, ?)",
                                                (read_order_item_id, read_order_id, article_id[0], STATUS, current_datetime))
                                            production_connection.commit()

                                        qty -= 1

                                # get the system-given variation id:
                                cursor.execute(
                                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                                    (read_order_item_id,))
                                variation = cursor.fetchall()
                                for data3 in variation:
                                    variation = str(data3[0])
                                    print("wp-wo-oimeta: Variation: " + variation)

                                    # use the system-give variation id to find related article-id's
                                    cursor.execute(
                                        "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                                        (variation,))
                                    article_id = cursor.fetchone()

                                    current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

                                    cursor.execute(
                                        "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident, time_stamp)"
                                        " VALUES (%s, %s, %s, %s, %s)",
                                        (read_order_item_id, read_order_id, article_id[0], STATUS, current_datetime))
                                    connection.commit()

                                    prod_cursor.execute(
                                        "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident, time_stamp)"
                                        " VALUES (?, ?, ?, ?, ?)",
                                        (read_order_item_id, read_order_id, article_id[0], STATUS, current_datetime))
                                    production_connection.commit()

                        cursor.execute(
                            "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
                        shop_oid_max_read = cursor.fetchone()
                        shop_oid_max = shop_oid_max_read[0]
                        connection.commit()

                        cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
                        cor_oid_max_read = cursor.fetchone()
                        cor_oid_max = cor_oid_max_read[0]
                        production_connection.commit()

        except KeyboardInterrupt:
            if self.connection_closed is False:
                self.connection_closed = True
                connection.close()
                production_connection.close()

        finally:
            if self.connection_closed is False:
                connection.close()
                production_connection.close()
            else:
                pass

if __name__ == '__main__':
    ShopInformationCollector().main()
