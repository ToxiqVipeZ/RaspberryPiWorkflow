#!/usr/bin/env python3
import sqlite3
import mysql.connector
import time

STATUS = "ORDER-IN"
MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "wordpress"
connection_closed = False

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"

try:
    while True:
        print("Baue Shop-Datenbankverbindung auf....")
        connection = mysql.connector.connect(host="169.254.0.3", user="pi", passwd="raspberry", db="wordpress")
        print("Baue Produktions-Datenbankverbindung auf....")
        production_connection = sqlite3.connect(
            SQLITE3_HOST)
        print("Datenbankverbindung steht!")
        cursor = connection.cursor()
        prod_cursor = production_connection.cursor()

        cursor.execute(
            "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
        shop_oid_max_read = cursor.fetchone()
        shop_oid_max = shop_oid_max_read[0]
        connection.commit()

        cursor.execute("SELECT MAX(order_id) FROM custom_order_receiver")
        cor_oid_max_read = cursor.fetchone()
        cor_oid_max = cor_oid_max_read[0]
        production_connection.commit()

        # Wenn die neuste Bestellung (shop_oid_max) bereits im custom_order_receiver(cor_oid_max) ist:
        # Bedeutet, es gibt keine neue Bestellung, welche noch nicht aufgenommen wurde
        if shop_oid_max == cor_oid_max:
            print("(shopInfoCol. if 1")
            while shop_oid_max == cor_oid_max:
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

        # Falls der custom order receiver leer ist, damit kein vergleich mit NULL erfolgt:
        if cor_oid_max == None:
            cor_oid_max = 0
        print(cor_oid_max)

        # Wenn es in der Tabelle eine Bestell-ID gibt, welche es noch nicht in custom_order_receiver gibt:
        # Neue Bestellung:
        if shop_oid_max > cor_oid_max:
            print("(shopInfoCol. if 2")
            cursor.execute(
                "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")
            resmaxorder = cursor.fetchone()
            for maxo in resmaxorder:
                print("Max Order ID:" + str(maxo))

            read_order_id = maxo

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
                    mv = (int(dats[0]))

                    if mv > 1:
                        print("(shopInfoCol. if 3 - mv")
                        while mv > 1:
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
                                "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident)"
                                " VALUES (%s, %s, %s, %s)",
                                (read_order_item_id, read_order_id, article_id[0], STATUS,))

                            connection.commit()

                            prod_cursor.execute(
                                "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident)"
                                " VALUES (?, ?, ?, ?)",
                                (read_order_item_id, read_order_id, article_id[0], STATUS,))

                            production_connection.commit()

                            mv = mv - 1

                    elif mv <= 1:
                        print("135 - mv <= 1")
                        cursor.execute(
                            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%variation%') AND order_item_id=%s",
                            (read_order_item_id,))
                        result1 = cursor.fetchall()

                        connection.commit()

                        for datr in result1:
                            print("VariationTableID: " + str(datr[0]))
                            variation_id = (str(datr[0]))

                        cursor.execute(
                            "SELECT sku AS article_id FROM wp_wc_product_meta_lookup WHERE product_id=%s",
                            (variation_id,))
                        article_id = cursor.fetchone()

                        connection.commit()

                        cursor.execute(
                            "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident)"
                            " VALUES (%s, %s, %s, %s)",
                            (read_order_item_id, read_order_id, article_id[0], STATUS,))

                        connection.commit()

                        prod_cursor.execute(
                            "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident)"
                            " VALUES (?, ?, ?, ?)",
                            (read_order_item_id, read_order_id, article_id[0], STATUS,))

                        production_connection.commit()

        elif shop_oid_max < cor_oid_max:
            print("shopInfoCol. Test 4")
            # die neueste Bestellung rausfinden

            cursor.execute(
                "SELECT MAX(order_id) FROM wp_woocommerce_order_items WHERE order_item_type like ('%line_item%')")

            resmaxorder = cursor.fetchone()
            for maxo in resmaxorder:
                print("Max Order ID: " + maxo)
            read_order_id = (maxo)

            connection.commit()

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

        cursor = connection.cursor()

        cursor.execute(
            "SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE meta_key like ('%qty%') AND order_item_id=%s",
            (read_order_item_id,))
        result1 = cursor.fetchall()

        connection.commit()

        for dats in result1:
            print("Menge: " + str(dats[0]))
        mv = (int(dats[0]))

        if mv > 1:
            print("shopInfoCol. 5 mv 2 / if mv >= 1")
            while mv > 1:
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
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident)"
                    " VALUES (%s, %s, %s, %s)",
                    (read_order_item_id, read_order_id, article_id[0], STATUS,))

                connection.commit()

                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident)"
                    " VALUES (?, ?, ?, ?)",
                    (read_order_item_id, read_order_id, article_id[0], STATUS))

                production_connection.commit()

                mv = mv - 1

        elif mv <= 1:
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
                    "INSERT INTO custom_order_receiver(order_item_id, order_id, article_id, status_ident)"
                    " VALUES (%s, %s, %s, %s)",
                    (read_order_item_id, read_order_id, article_id[0], STATUS,))

                connection.commit()

                prod_cursor.execute(
                    "INSERT INTO shop_info_table(order_item_id, order_id, article_id, status_ident)"
                    " VALUES (?, ?, ?, ?)",
                    (read_order_item_id, read_order_id, article_id[0], STATUS))

                production_connection.commit()

except KeyboardInterrupt:
    connection.close()
    production_connection.close()
    connection_closed = True

finally:
    if not connection_closed:
        connection.close()
        production_connection.close()
