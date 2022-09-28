import sqlite3
import time
from threading import Thread
from . import Client

DATABASE_PATH = "/home/pi/ServerFiles/Database/productionDatabase.db"


class StorageWorkerBackend:
    feedback_message = "None"

    def set_feedback_message(self, message):
        self.feedback_message = message

    def stock_data(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT * "
                  "FROM part_storages_table "
                  "WHERE part_amount <= min_amount")
        fetch = c.fetchall()
        connection.commit()
        connection.close()

        if fetch is not None:
            return fetch
        else:
            return ""

    def min_amount_check(self, cassette_id, part_amount):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT min_amount, part_amount "
                  "FROM part_storages_table "
                  "WHERE in_cassettes=(?)", (cassette_id,))
        amount = c.fetchone()
        connection.commit()
        connection.close()
        print(amount)
        if amount is not None:
            if amount[0] is not None and amount[1] is not None:
                min_amount = amount[0]
                part_amount_in_store = amount[1]

                if part_amount_in_store - int(part_amount) < 0:
                    return 2
                elif min_amount >= part_amount_in_store - int(part_amount):
                    return 1
                elif min_amount < part_amount_in_store - int(part_amount):
                    return 0

    def cassette_out_triggered(self, cassette_id, part_id, part_amount):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT part_amount "
                  "FROM part_storages_table "
                  "WHERE in_cassettes=(?)", (cassette_id,))
        part_amount_in_store = c.fetchone()
        if part_amount_in_store[0] is not None:
            part_amount_in_store = part_amount_in_store[0]
        c.execute("UPDATE part_storages_table "
                  "SET part_amount=(?) "
                  "WHERE part_id=(?)",
                  (part_amount_in_store - int(part_amount), part_id))
        connection.commit()
        connection.close()

    def packing_completed(self, article_id, not_in_cassettes):

        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        print(not_in_cassettes)
        print(not_in_cassettes[0])
        print(article_id)
        part_amount_in_store_list = []
        part_id_list = []
        part_amount_list = []
        part_not_in_store = ""
        not_in_store_flag = False

        # not_in_cassettes = [part_id, part_amount, '-']
        # item[0] = part_id
        # item[1] = part_amount
        for item in not_in_cassettes:
            c.execute("SELECT part_amount "
                      "FROM part_storages_table "
                      "WHERE part_id=(?)", (item[0],))
            part_amount_in_store = c.fetchone()
            connection.commit()
            connection.close()
            if part_amount_in_store is None:
                not_in_store_flag = True
                part_not_in_store = item[0]
            else:
                if part_amount_in_store is not None:
                    if part_amount_in_store[0] is not None:
                        part_amount_in_store_list.append(part_amount_in_store[0])
                        part_amount_list.append(item[1])
                        part_id_list.append(item[0])

        if not not_in_store_flag:
            for x in range(0, len(part_amount_in_store_list)):
                if part_amount_in_store_list is not None:
                    if part_amount_in_store_list[x] is not None:
                        part_amount_in_store = part_amount_in_store_list[x]
                        part_amount = part_amount_list[x]
                        part_id = part_id_list[x]
                        c.execute("UPDATE part_storages_table "
                                  "SET part_amount=(?) "
                                  "WHERE part_id=(?)",
                                  (part_amount_in_store - int(part_amount), part_id))
                        connection.commit()
                        connection.close()
                        self.setting_rfid(article_id)
        else:
            self.set_feedback_message("Eins / oder mehrere Teile dieses\n"
                                        "Artikels, sind nicht im Lager enthalten!\n"
                                        "Zumindest fehlt: " + str(part_not_in_store))

    def setting_rfid(self, article_id):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()

        station = "01"
        variation = article_id[8:]
        article_id = article_id[:7]

        c.execute("SELECT procedure FROM article_procedure_table WHERE article_id=(?)", (article_id,))
        procedure = c.fetchone()
        if procedure is not None:
            if procedure[0] is not None:
                procedure = procedure[0]
        else:
            self.set_feedback_message("Produktions-vorgang für diesen Artikel ist nicht angelegt: " + article_id)

        rfid = station + procedure + variation
        self.statistic_tracker("IN", rfid)
        new_rfid = Client.send(Client.SENDING_RFID, rfid) + procedure + variation
        self.statistic_tracker("OUT", new_rfid)
        print("New RFID: " + rfid + " -> " + new_rfid)
        Client.send(Client.DISCONNECT_MESSAGE)

        connection.commit()
        connection.close()


    def statistic_tracker(self, in_or_out, rfid_code):
        station_number = "01"
        print("statistic_tracker station_number: " + station_number)
        if in_or_out == "IN":
            Thread(target=Client.send(Client.TRACKING_STATS_IN, rfid_code, station_number)).start()
        elif in_or_out == "OUT":
            Thread(target=Client.send(Client.TRACKING_STATS_OUT, rfid_code, station_number)).start()

    def delayed_destroyer(self, item, time_in_s):
        time.sleep(time_in_s)
        item.destroy()

    def get_article_to_pack(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT * FROM process_time_table WHERE station=\"01\" ORDER BY process_id ASC")
        articles_to_pack = c.fetchall()

        if articles_to_pack is not []:
            if len(articles_to_pack) > 0:
                next_article_to_pack = articles_to_pack[0]
                c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=(?)",
                          (str(next_article_to_pack[1]),))
                article_parts_rel = c.fetchone()
                parts = article_parts_rel[1][2:-2].split("\', \'")
                amounts = article_parts_rel[2][2:-2].split("\', \'")
                part_list = []
                part_list.append([article_parts_rel[0], "", ""])
                # print(part_list)
                if article_parts_rel is not None:
                    for x in range(0, len(parts)):
                        c.execute("SELECT cassette_id FROM cassette_management_table WHERE cassette_contains=(?)",
                                  (parts[x],))
                        cassette_id = c.fetchone()
                        if cassette_id is not None:
                            if cassette_id[0] is not None:
                                part_list.append([parts[x], amounts[x], cassette_id[0]])
                            else:
                                part_list.append([parts[x], amounts[x], "0"])
                        else:
                            part_list.append([parts[x], amounts[x], "-"])
                    return articles_to_pack, part_list

                elif article_parts_rel is None:
                    print("Artikel-Teile-Relation nicht angelegt!")
                    return articles_to_pack, 0
            elif len(articles_to_pack) <= 0:
                print("Keine Artikel die auf Bearbeitung warten.")
                return 0, 0
        elif articles_to_pack is []:
            print("Keine Artikel die auf Bearbeitung warten.")
            return 0, 0

        connection.close()

    def main(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()

        connection.commit()
        connection.close()


if __name__ == '__main__':
    StorageWorkerBackend().get_article_to_pack()
