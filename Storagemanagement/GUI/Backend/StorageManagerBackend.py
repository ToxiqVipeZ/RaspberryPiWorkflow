import sqlite3
import mysql.connector
import time

DATABASE_PATH = "/home/pi/ServerFiles/Database/productionDatabase.db"


class StorageManagerBackend:
    MYSQL_HOST = "169.254.0.3"
    MYSQL_USER = "pi"
    MYSQL_PASSWD = "raspberry"
    MYSQL_DB = "production"

    feedback_message = "None"

    def set_feedback_message(self, message):
        self.feedback_message = message

    def delayed_destroyer(self, item, time_in_s):
        time.sleep(time_in_s)
        item.destroy()

    def delete_part_from_store(self, part_id, part_amount):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)
        c = connection.cursor()
        c.execute("SELECT part_id, part_amount FROM part_storages_table WHERE part_id=%s", (part_id,))
        part_data_from_table = c.fetchone()

        if part_data_from_table is not None:
            part_amount_from_table = part_data_from_table[1]

            c.execute("SELECT cassette_id FROM cassette_management_table WHERE cassette_contains=%s", (part_id,))
            cassette_id = c.fetchone()

            if part_amount == "":
                part_amount = None

            if part_amount is None:
                if cassette_id is not None:
                    cassette_id = cassette_id[0]
                    c.execute("UPDATE cassette_management_table SET cassette_contains=%s WHERE cassette_id=%s",
                              (None, cassette_id))
                    connection.commit()
                    c.execute("DELETE FROM part_storages_table WHERE part_id=%s", (part_id,))
                    connection.commit()

                elif cassette_id is None:
                    c.execute("DELETE FROM part_storages_table WHERE part_id=%s", (part_id,))
                    connection.commit()

            elif part_amount is not None:
                part_amount = int(part_amount)
                if part_amount_from_table >= part_amount:
                    new_part_amount = part_amount_from_table - part_amount
                    c.execute("UPDATE part_storages_table SET part_amount=%s WHERE part_id=%s",
                              (new_part_amount, part_id))
                    connection.commit()
                    self.set_feedback_message(str(part_amount) + " Stück von \n" + part_id + " gelöscht")
                elif part_amount_from_table < part_amount:
                    self.set_feedback_message("Es gibt nur " + str(part_amount_from_table) +
                                              "\n Stücke dieses Teils im Lager.")

        connection.close()

    def save_part_to_store(self, part_id, part_amount, part_min_amount):

        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)
        c = connection.cursor()
        c.execute("SELECT * FROM part_storages_table")
        parts = c.fetchall()
        c.execute("SELECT cassette_id FROM cassette_management_table WHERE cassette_contains=%s", (part_id,))
        cassette_id = c.fetchone()

        if cassette_id is not None:
            cassette_id = cassette_id[0]
        if cassette_id is None:
            cassette_id = 0

        not_included = True

        for x in range(0, len(parts)):
            if part_id == parts[x][0]:
                c.execute("UPDATE part_storages_table "
                          "SET part_amount=%s, "
                          "min_amount=%s, "
                          "in_cassettes=%s "
                          "WHERE part_id=%s",
                          (part_amount,
                           part_min_amount,
                           cassette_id,
                           part_id))
                connection.commit()
                not_included = False
                self.feedback_message = "Teil aktualisiert."

        if not_included:
            c.execute("INSERT INTO part_storages_table "
                      "VALUES (%s, %s, %s, %s)",
                      (part_id,
                       part_amount,
                       part_min_amount,
                       cassette_id))
            connection.commit()
            self.feedback_message = "Teil hinzugefügt."

        connection.close()

    def get_stored_parts(self):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)
        c = connection.cursor()
        c.execute("SELECT * FROM part_storages_table")
        stored_parts = c.fetchall()
        connection.close()
        return stored_parts

    def get_article_relations(self):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)
        c = connection.cursor()
        c.execute("SELECT article_id FROM article_parts_relation_table")
        article_parts_relation_table = c.fetchall()
        connection.close()
        return article_parts_relation_table

    def get_cassette_contains(self, cassette_id):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        c.execute("SELECT cassette_contains "
                  "FROM cassette_management_table WHERE cassette_id=%s", (cassette_id,))
        cassette_contains = c.fetchone()

        if cassette_contains is not None:
            if cassette_contains[0] is not None:
                cassette_contains = cassette_contains[0]
            else:
                cassette_contains = None
        else:
            cassette_contains = None

        connection.close()
        return cassette_contains

    def get_contains_amount(self, cassette_id):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        c.execute("SELECT contains_max_amount "
                  "FROM cassette_management_table WHERE cassette_id=%s", (cassette_id,))
        contains_max_amount = c.fetchone()

        if contains_max_amount is not None:
            if contains_max_amount[0] is not None:
                contains_max_amount = contains_max_amount[0]
            else:
                contains_max_amount = None
        else:
            contains_max_amount = None

        connection.close()
        return contains_max_amount

    def save_cassette_contains(self, casette_id, cassette_contains, contains_max_amount):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        c.execute("UPDATE cassette_management_table "
                  "SET cassette_contains=%s, "
                  "contains_max_amount=%s "
                  "WHERE cassette_id=%s",
                  (str(cassette_contains),
                   contains_max_amount,
                   casette_id))
        connection.commit()
        print(cassette_contains)

        c.execute("SELECT part_id FROM part_storages_table "
                  "WHERE in_cassettes=%s", (casette_id,))
        part_id = c.fetchone()
        if part_id is not None:
            part_id = part_id[0]
        if cassette_contains == "":
            print("test")
            c.execute("UPDATE part_storages_table "
                      "SET in_cassettes=%s "
                      "WHERE part_id=%s",
                      (0, part_id))
            connection.commit()
        else:
            c.execute("UPDATE part_storages_table "
                      "SET in_cassettes=%s "
                      "WHERE part_id=%s",
                      (casette_id, cassette_contains))
            connection.commit()

        connection.close()

    def lookup_article_parts_relations(self, article_id):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        # article-id from article-id textbox
        article_id = article_id.get("1.0", "end-1c")

        # checking if article-id is already inside the databank
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=%s", (article_id,))
        article_id_included = c.fetchone()

        if article_id_included is not None:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" in Datenbank gefunden.")
        else:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" nicht in Datenbank gefunden.")

        connection.commit()
        connection.close()
        return article_id_included

    def delete_article_parts_relations(self, article_id):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        # article-id from article-id textbox
        article_id = article_id.get("1.0", "end-1c")

        # checking if article-id is already inside the databank
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=%s", (article_id,))
        article_id_included = c.fetchone()

        if article_id_included is not None:
            c.execute("DELETE FROM article_parts_relation_table WHERE article_id=%s", (article_id,))
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" aus Datenbank gelöscht.")
        else:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" nicht in Datenbank enthalten.")

        connection.commit()
        connection.close()

    def save_article_parts_relations(self, article_id, part_numbers):
        connection = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                                             passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB)

        # cursor instance:
        c = connection.cursor()

        # article-id from article-id textbox
        article_id = article_id.get("1.0", "end-1c")

        # part numbers from the part numbers textbox
        part_numbers_list = part_numbers.get("1.0", "end-1c")
        part_numbers_list = part_numbers_list.split("\n")

        # empty lists for the amount (...x123) and the final part numbers list after formatting
        part_numbers_list_amounts = []
        part_numbers_list_final = []

        # feeding the empty lists with the formatted values
        for i in range(0, len(part_numbers_list)):
            part_number = part_numbers_list[i].split("x")[1]
            part_numbers_list_amounts.append(part_number)
            part_numbers_list_final.append(part_numbers_list[i][:-2])

        # checking if article-id is already inside the databank
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=%s", (article_id,))
        article_id_included = c.fetchone()

        # if article-id is not inside the databank:
        if article_id_included is None:
            c.execute("INSERT INTO article_parts_relation_table "
                      "VALUES (%s, %s, %s)",
                      (article_id,
                       str(part_numbers_list_final),
                       str(part_numbers_list_amounts)))
            connection.commit()
            self.set_feedback_message("Neue \"Artikel-Teilenummer\" -zuordnung gespeichert.")
        # if the article-id is already inside the databank:
        else:
            c.execute("UPDATE article_parts_relation_table "
                      "SET part_id_list=%s, "
                      "part_id_list_amounts=%s "
                      "WHERE article_id=%s",
                      (str(part_numbers_list_final),
                       str(part_numbers_list_amounts),
                       article_id))
            connection.commit()
            self.set_feedback_message("Bestehende \"Artikel-Teilenummer\" -zuordnung aktualisiert.")

        # closing the databank connection:
        connection.close()

        # test-prints:
        print(article_id)
        print(part_numbers_list_final)
        print(part_numbers_list_amounts)
