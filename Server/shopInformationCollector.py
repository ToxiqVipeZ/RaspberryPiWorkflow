#!/usr/bin/env python3
import sqlite3

import mysql.connector
import time

global read_order_item_id
x = 5


def Status_log(read_order_item_id):
    cursor.execute("SELECT MAX(ident_number) FROM custom_order_receiver LIMIT 0, 1")
    prod_cursor.execute("SELECT MAX(production_number) FROM shop_info_table LIMIT 0, 1")
    Produktionsnummer = cursor.fetchone()
    print("Produktionsnummer: " + str(Produktionsnummer[0]))
    print("-------------------------------")

    Status = "Bestellung IN"

    cursor.execute("UPDATE custom_order_receiver SET status_ident=%s WHERE order_item_id LIKE %s", (Status, read_order_item_id,))
    prod_cursor.execute("UPDATE shop_info_table SET status_ident=(?) WHERE order_item_id LIKE (?)", (Status, read_order_item_id,))
    connection.commit()
    production_connection.commit()


try:
    while x > 1:
        connection = mysql.connector.connect(host="169.254.0.3", user="FRANK", passwd="$Ute2511%", db="wordpress2")
        production_connection = sqlite3.connect(
            "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")
        cursor = connection.cursor()
        prod_cursor = production_connection.cursor()

        cursor.execute(
            "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
        shop_oid_max_read = cursor.fetchone()
        shop_oid_max = (shop_oid_max_read)
        connection.commit()

        cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
        cor_oid_max_read = cursor.fetchone()
        cor_oid_max = (cor_oid_max_read)
        production_connection.commit()

        # Wenn die neuste Bestellung (shop_oid_max) bereits im custom_order_receiver(cor_oid_max) ist:
        if shop_oid_max == cor_oid_max:
            while shop_oid_max == cor_oid_max:
                cursor.execute(
                    "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
                shop_oid_max_read = cursor.fetchone()
                shop_oid_max = (shop_oid_max_read)
                connection.commit()

                cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
                cor_oid_max_read = cursor.fetchone()
                cor_oid_max = (cor_oid_max_read)
                connection.commit()

                print("Warte 5s auf Bestelleingangsscan")
                time.sleep(5)

        # Wenn es in der Tabelle eine Bestell-ID gibt, welche es noch nicht in custom_order_receiver gibt:
        if shop_oid_max > cor_oid_max:
            cursor.execute(
                "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")

            resmaxorder = cursor.fetchone()
            for maxo in resmaxorder:
                print("Max Order ID:" + str(maxo))

            read_order_id = (maxo)

            # Order item id rausfinden um auf naechste tabelle mit meta key auf meta value qty zugreifen zu koennen:
            cursor.execute(
                "SELECT order_item_ID FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%') AND order_id=%s",
                (read_order_id,))
            result = cursor.fetchall()
            connection.commit()

            # order item id's rausfinden:
            print("Order item IDs:")
            for data in result:
                print("ID: " + str(data[0]))
                read_order_item_id = (str(data[0]))

                cursor = connection.cursor()

                cursor.execute(
                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
                    (read_order_item_id,))
                result1 = cursor.fetchall()
                connection.commit()

                # Bestellte Menge des items mit der order_item_ID rausfinden
                for dats in result1:
                    print("Menge: " + str(dats[0]))
                    mv = (str(dats[0]))
                    mv = (int(dats[0]))

                    if mv > 1:
                        while mv >= 1:
                            cursor.execute(
                                "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                                (read_order_item_id,))
                            result1 = cursor.fetchall()

                            connection.commit()

                            for datr in result1:
                                print("Variation: " + str(datr[0]))
                                mvv = (str(datr[0]))

                            cursor.execute(
                                "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                                (mvv,))
                            article_id = cursor.fetchone()

                            cursor.execute(
                                "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                                (read_order_item_id, read_order_id, article_id[0],))
                            prod_cursor.execute(
                                "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                                (read_order_item_id, read_order_id, article_id[0],))
                            Status_log(read_order_item_id)
                            connection.commit()
                            production_connection.commit()
                            mv = mv - 1

                    else:
                        cursor.execute(
                            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                            (read_order_item_id,))
                        result1 = cursor.fetchall()

                        connection.commit()

                        for datr in result1:
                            print("Variation: " + str(datr[0]))
                        mvv = (str(datr[0]))

                        cursor.execute(
                            "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                            (mvv,))
                        article_id = cursor.fetchone()

                        cursor.execute(
                            "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                            (read_order_item_id, read_order_id, article_id[0],))
                        prod_cursor.execute(
                            "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                            (read_order_item_id, read_order_id, article_id[0],))
                        Status_log(read_order_item_id)
                        connection.commit()
                        production_connection.commit()
        else:
            # die neueste Bestellung rausfinden

            cursor.execute(
                "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")

            resmaxorder = cursor.fetchone()
            for maxo in resmaxorder:
                print("Max Order ID: " + maxo)
            read_order_id = (maxo)

            ########################################################################################################

            # Order item id rausfinden um auf naechste tabelle mit meta key auf meta value qty zugreifen zu koennen
        cursor.execute(
            "SELECT order_item_ID FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%') AND order_id=%s",
            (read_order_id,))
        result = cursor.fetchall()
        connection.commit()

        print("Order item IDs:")

        for data in result:
            print("ID: " + str(data[0]))
        read_order_item_id = (str(data[0]))

        ############################################################################################################

        cursor = connection.cursor()

        cursor.execute(
            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
            (read_order_item_id,))
        result1 = cursor.fetchall()

        connection.commit()

        for dats in result1:
            print("Menge: " + str(dats[0]))
        mv = (str(dats[0]))
        mv = (int(dats[0]))

        if mv > 1:
            while mv >= 1:
                cursor.execute(
                    "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                    (read_order_item_id,))
                result1 = cursor.fetchall()

                connection.commit()

                for datr in result1:
                    print("Variation: " + str(datr[0]))
                    mvv = (str(datr[0]))

                cursor.execute("SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                               (mvv,))
                article_id = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                    (read_order_item_id, read_order_id, article_id[0],))
                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                    (read_order_item_id, read_order_id, article_id[0],))
                Status_log(read_order_item_id)
                connection.commit()
                production_connection.commit()
                mv = mv - 1

        else:
            cursor.execute(
                "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                (read_order_item_id,))
            result1 = cursor.fetchall()

            connection.commit()

            for datr in result1:
                print("Variation: " + str(datr[0]))
                mvv = (str(datr[0]))

                cursor.execute("SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                               (mvv,))
                article_id = cursor.fetchone()

                cursor.execute(
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id) VALUES (%s, %s, %s)",
                    (read_order_item_id, read_order_id, article_id[0],))
                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id) VALUES (?, ?, ?)",
                    (read_order_item_id, read_order_id, article_id[0],))
                Status_log(read_order_item_id)
                connection.commit()
                production_connection.commit()

except KeyboardInterrupt:
    connection.close()
    production_connection.close()

