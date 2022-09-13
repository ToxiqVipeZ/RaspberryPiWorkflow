import sqlite3
import time

DATABASE_PATH = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"


class StorageWorkerBackend:
    feedback_message = "None"

    def set_feedback_message(self, message):
        self.feedback_message = message

    def delayed_destroyer(self, item, time_in_s):
        time.sleep(time_in_s)
        item.destroy()

    def get_article_to_pack(self):
        connection = sqlite3.connect(DATABASE_PATH)
        c = connection.cursor()
        c.execute("SELECT * FROM process_time_table WHERE station=\"01\" ORDER BY process_id ASC")
        articles_to_pack = c.fetchall()
        print(articles_to_pack)

        if articles_to_pack is not []:
            next_article_to_pack = articles_to_pack[0]
            print(next_article_to_pack)
            c.execute("SELECT * FROM article_parts_relation_table WHERE article_id=(?)",
                      (str(next_article_to_pack[1]),))
            article_parts_rel = c.fetchone()
            parts = article_parts_rel[1][2:-2].split("\', \'")
            amounts = article_parts_rel[2][2:-2].split("\', \'")
            print(parts)
            print(amounts)
            part_list = []
            part_list.append([article_parts_rel[0], "", ""])
            #print(part_list)
            if article_parts_rel is not None:
                for x in range(0, len(parts)):
                    print(parts[x])
                    c.execute("SELECT cassette_id FROM cassette_management_table WHERE cassette_contains=(?)",
                              (parts[x],))
                    cassette_id = c.fetchone()
                    if cassette_id is not None:
                        if cassette_id[0] is not None:
                            print("cassette_m_tab" + str(cassette_id[0]))
                            part_list.append([parts[x], amounts[x], cassette_id[0]])
                        else:
                            part_list.append([parts[x], amounts[x], "0"])
                    else:
                        part_list.append([parts[x], amounts[x], "-"])
                print(part_list)
                return articles_to_pack, part_list

            elif article_parts_rel is None:
                print("Artikel-Teile-Relation nicht angelegt!")
                return articles_to_pack, 0

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
