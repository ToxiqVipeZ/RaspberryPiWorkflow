import sqlite3
import time

DATABASE_PATH = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"


class StorageManagerBackend:
    feedback_message = "None"

    def set_feedback_message(self, message):
        self.feedback_message = message

    def delayed_destroyer(self, item, time_in_s):
        time.sleep(time_in_s)
        item.destroy()

    def save_part_to_store(self, part_id, part_amount):

        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT * FROM part_storages_table")
        parts = c.fetchall()
        c.execute("SELECT cassette_id FROM cassette_management_table WHERE cassette_contains=(?)", (part_id,))
        cassette_id = c.fetchone()

        if cassette_id is not None:
            cassette_id = cassette_id[0]
        if cassette_id is None:
            cassette_id = 0

        not_included = True

        for x in range(0, len(parts)):
            if part_id == parts[x][0]:
                c.execute("UPDATE part_storages_table "
                          "SET part_amount=(?), "
                          "in_cassettes=(?) "
                          "WHERE part_id=(?)",
                          (part_amount,
                           cassette_id,
                           part_id))
                connection.commit()
                not_included = False
                self.feedback_message = "Teil aktualisiert."

        if not_included:
            c.execute("INSERT INTO part_storages_table "
                      "VALUES (?,?,?)",
                      (part_id,
                       part_amount,
                       cassette_id))
            connection.commit()
            self.feedback_message = "Teil hinzugefügt."

        connection.close()

    def get_stored_parts(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT * FROM part_storages_table")
        stored_parts = c.fetchall()
        connection.close()
        return stored_parts

    def get_article_relations(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT article_id FROM article_parts_relation_table")
        article_parts_relation_table = c.fetchall()
        connection.close()
        return article_parts_relation_table

    def get_cassette_contains(self, cassette_id):
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        c = connection.cursor()

        c.execute("SELECT cassette_contains "
                  "FROM cassette_management_table WHERE cassette_id=(?)", (cassette_id,))
        cassette_contains = c.fetchone()[0]

        print(cassette_contains)
        connection.close()
        return cassette_contains

    def get_contains_amount(self, cassette_id):
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        c = connection.cursor()

        c.execute("SELECT contains_amount "
                  "FROM cassette_management_table WHERE cassette_id=(?)", (cassette_id,))
        contains_amount = c.fetchone()[0]

        print(contains_amount)
        connection.close()
        return contains_amount

    def save_cassette_contains(self, casette_id, cassette_contains, contains_amount):
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        c = connection.cursor()

        c.execute("UPDATE cassette_management_table "
                  "SET cassette_contains=(?), "
                  "contains_amount=(?) "
                  "WHERE cassette_id=(?)",
                  (str(cassette_contains),
                   contains_amount,
                   casette_id))

        connection.commit()
        connection.close()

    def lookup_article_parts_relations(self, article_id):
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        c = connection.cursor()

        # article-id from article-id textbox
        article_id = article_id.get("1.0", "end-1c")

        # checking if article-id is already inside the databank
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=(?)", (article_id,))
        article_id_included = c.fetchone()

        if article_id_included is not None:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" in Datenbank gefunden.")
        else:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" nicht in Datenbank gefunden.")

        connection.commit()
        connection.close()
        return article_id_included

    def delete_article_parts_relations(self, article_id):
        connection = sqlite3.connect(DATABASE_PATH)

        # cursor instance:
        c = connection.cursor()

        # article-id from article-id textbox
        article_id = article_id.get("1.0", "end-1c")

        # checking if article-id is already inside the databank
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=(?)", (article_id,))
        article_id_included = c.fetchone()

        if article_id_included is not None:
            c.execute("DELETE FROM article_parts_relation_table WHERE article_id=(?)", (article_id,))
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" aus Datenbank gelöscht.")
        else:
            self.set_feedback_message("Artikel-ID: \"" + str(article_id) + "\" nicht in Datenbank enthalten.")

        connection.commit()
        connection.close()

    def save_article_parts_relations(self, article_id, part_numbers):
        connection = sqlite3.connect(DATABASE_PATH)

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
        c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=(?)", (article_id,))
        article_id_included = c.fetchone()

        # if article-id is not inside the databank:
        if article_id_included is None:
            c.execute("INSERT INTO article_parts_relation_table "
                      "VALUES (?,?,?)",
                      (article_id,
                       str(part_numbers_list_final),
                       str(part_numbers_list_amounts)))
            connection.commit()
            self.set_feedback_message("Neue \"Artikel-Teilenummer\" -zuordnung gespeichert.")
        # if the article-id is already inside the databank:
        else:
            c.execute("UPDATE article_parts_relation_table "
                      "SET part_id_list=(?), "
                      "part_id_list_amounts=(?) "
                      "WHERE article_id=(?)",
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
