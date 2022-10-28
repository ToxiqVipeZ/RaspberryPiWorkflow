import time
import mysql.connector
import sqlite3


MYSQL_HOST = "169.254.0.3"
MYSQL_USER = "pi"
MYSQL_PASSWD = "raspberry"
MYSQL_DB = "production"


class AcquiringDashData:

    def main(self):
        try:
            while True:
                dashboard_data_connection = sqlite3.connect("../Database/DashboardDatabase.db")
                dashboard_c = dashboard_data_connection.cursor()

                # cursor instance:
                connection = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                                     passwd=MYSQL_PASSWD, db=MYSQL_DB)
                c = connection.cursor()

                print("Copying Data...")
                c.execute("SELECT * FROM process_time_table")
                data = c.fetchall()

                dashboard_c.execute("SELECT * FROM process_time_table")
                dash_data = dashboard_c.fetchall()

                if len(data) != len(dash_data):
                    print("full copy.")
                    dashboard_c.execute("DELETE FROM process_time_table")
                    dashboard_data_connection.commit()

                    c.execute("SELECT * FROM process_time_table")
                    data = c.fetchall()

                    dashboard_c.executemany(
                        "INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
                    dashboard_data_connection.commit()

                    c.execute("SELECT * FROM process_time_table")
                    data = c.fetchall()

                    dashboard_c.execute("SELECT * FROM process_time_table")
                    dash_data = dashboard_c.fetchall()

                # if len(data) > len(dash_data):
                #     dash_data_len = len(dash_data)
                #     c.execute("SELECT MAX(entry_count) FROM process_time_table")
                #     entry_nr = c.fetchone()
                #     if entry_nr is not None:
                #         entry_nr = entry_nr[0]
                #     print(entry_nr)
                #     c.execute("SELECT * FROM process_time_table WHERE entry_count=%s", (entry_nr, ))
                #     data = c.fetchone()
                #     dashboard_c.execute("INSERT INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
                #     dashboard_data_connection.commit()

                if len(data) == len(dash_data):
                    print("insert or replace.")
                    c.execute("SELECT * FROM process_time_table")
                    data = c.fetchall()

                    dashboard_c.executemany("INSERT or REPLACE INTO process_time_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
                    dashboard_data_connection.commit()

                time.sleep(0.5)

        finally:
            dashboard_data_connection.close()
            connection.close()

if __name__ == '__main__':
    AcquiringDashData().main()