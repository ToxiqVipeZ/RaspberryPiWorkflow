#!/usr/bin/env python3
import sqlite3

import mysql.connector
import time

global OiID
x = 5


def Status_log(OiID):
    cursor.execute("SELECT MAX(ident_number) FROM custom_order_receiver LIMIT 0, 1")
    prod_cursor.execute("SELECT MAX(ident_number) FROM shop_info_table LIMIT 0, 1")
    Produktionsnummer = cursor.fetchone()
    print(Produktionsnummer[0])

    Status = "Bestellung IN"

    print("test" + str(OiID))
    cursor.execute("UPDATE custom_order_receiver SET status_ident=%s WHERE order_item_id LIKE %s", (Status, OiID,))
    prod_cursor.execute("UPDATE shop_info_table SET status_ident=(?) WHERE order_item_id LIKE (?)", (Status, OiID,))
    connection.commit()
    production_connection.commit()


while x > 1:
    connection = mysql.connector.connect(host="169.254.0.3", user="FRANK", passwd="$Ute2511%", db="wordpress2")
    production_connection = sqlite3.connect("C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")
    cursor = connection.cursor()
    prod_cursor = production_connection.cursor()

    cursor.execute("SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
    orderitemmax = cursor.fetchone()
    oimax = (orderitemmax)
    connection.commit()

    cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
    bestellergebnismax = cursor.fetchone()
    bemax = (bestellergebnismax)
    connection.commit()

    if oimax == bemax:
        while oimax == bemax:
            cursor.execute(
                "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
            orderitemmax = cursor.fetchone()
            oimax = (orderitemmax)
            connection.commit()

            cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
            bestellergebnismax = cursor.fetchone()
            bemax = (bestellergebnismax)
            connection.commit()

            print("Warten")

            time.sleep(5)

            if oimax > bemax:
                cursor.execute(
                    "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")

                resmaxorder = cursor.fetchone()
                for maxo in resmaxorder:
                    print("Max Order ID:")
                    print(maxo)

                OID = (maxo)

                ########################################################################################################

                # Order item id rausfinden um auf naechste tabelle mit meta key auf meta value qty zugreifen zu koennen

                cursor.execute(
                    "SELECT order_item_ID FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%') AND order_id=%s",
                    (OID,))
                result = cursor.fetchall()
                connection.commit()

                print("Order item IDs:")

                for data in result:
                    print(str(data[0]))
                    OiID = (str(data[0]))

                    cursor = connection.cursor()

                    cursor.execute(
                        "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
                        (OiID,))
                    result1 = cursor.fetchall()

                    connection.commit()

                    for dats in result1:
                        print(str(dats[0]))
                        mv = (str(dats[0]))
                        mv = (int(dats[0]))

                        if mv > 1:
                            while mv >= 1:
                                cursor.execute(
                                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                                    (OiID,))
                                result1 = cursor.fetchall()

                                connection.commit()

                                for datr in result1:
                                    print(str(datr[0]))
                                    mvv = (str(datr[0]))

                                cursor.execute(
                                    "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                                    (mvv,))
                                article_id = cursor.fetchone()

                                cursor.execute(
                                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                                    (OiID, OID, article_id[0],))
                                prod_cursor.execute(
                                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                                    (OiID, OID, article_id[0],))
                                Status_log(OiID)
                                connection.commit()
                                production_connection.commit()
                                mv = mv - 1

                        else:
                            cursor.execute(
                                "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                                (OiID,))
                            result1 = cursor.fetchall()

                            connection.commit()

                            for datr in result1:
                                print(str(datr[0]))
                            mvv = (str(datr[0]))

                            cursor.execute(
                                "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                                (mvv,))
                            article_id = cursor.fetchone()

                            cursor.execute(
                                "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                                (OiID, OID, article_id[0],))
                            prod_cursor.execute(
                                "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                                (OiID, OID, article_id[0],))
                            Status_log(OiID)
                            connection.commit()
                            production_connection.commit()
            else:
                # die neueste Bestellung rausfinden

                cursor.execute(
                    "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")

                resmaxorder = cursor.fetchone()
                for maxo in resmaxorder:
                    print("Max Order ID:")
                print(maxo)

                OID = (maxo)

        ########################################################################################################

        # Order item id rausfinden um auf naechste tabelle mit meta key auf meta value qty zugreifen zu koennen

        cursor.execute(
            "SELECT order_item_ID FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%') AND order_id=%s",
            (OID,))
        result = cursor.fetchall()
        connection.commit()

        print("Order item IDs:")

        for data in result:
            print(str(data[0]))
        OiID = (str(data[0]))

        ############################################################################################################

        cursor = connection.cursor()

        cursor.execute(
            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
            (OiID,))
        result1 = cursor.fetchall()

        connection.commit()

        for dats in result1:
            print(str(dats[0]))
        mv = (str(dats[0]))
        mv = (int(dats[0]))

        if mv > 1:
            while mv >= 1:
                cursor.execute(
                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                    (OiID,))
                result1 = cursor.fetchall()

                connection.commit()

                for datr in result1:
                    print(str(datr[0]))
                    mvv = (str(datr[0]))

                cursor.execute("SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                               (mvv,))
                article_id = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                    (OiID, OID, article_id[0],))
                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                    (OiID, OID, article_id[0],))
                Status_log(OiID)
                connection.commit()
                production_connection.commit()
                mv = mv - 1

        else:
            cursor.execute(
                "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                (OiID,))
            result1 = cursor.fetchall()

            connection.commit()

            for datr in result1:
                print(str(datr[0]))
                mvv = (str(datr[0]))

                cursor.execute("SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                               (mvv,))
                article_id = cursor.fetchone()

                cursor.execute(
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                    (OiID, OID, article_id[0],))
                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                    (OiID, OID, article_id[0],))
                Status_log(OiID)
                connection.commit()
                production_connection.commit()
