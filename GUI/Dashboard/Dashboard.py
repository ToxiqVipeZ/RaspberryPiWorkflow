import pandas as pd
from dash import Dash, html, dcc
import sqlite3
import plotly.express as px

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"
table_head = ("production number", "article id", "order id",
              "station\t", "next station\t", "last station\t",
              "process start", "process end")
table_head_stations = ("Artikel-ID: ", "Station: ")

print("Baue Produktions-Datenbankverbindung auf....")
production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbankverbindung steht!")
prod_cursor = production_connection.cursor()


def generate_table(data_frame, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(table_head[col]) for col in data_frame.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
            ]) for i in range(min(len(data_frame), max_rows))
        ])
    ])


def generate_stations_await(data_frame, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(table_head_stations[col]) for col in data_frame.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
            ]) for i in range(min(len(data_frame), max_rows))
        ])
    ])


app = Dash(__name__)

prod_cursor.execute("SELECT * FROM process_time_table ORDER BY process_id")
table = prod_cursor.fetchall()
print(str(table))

prod_cursor.execute("SELECT DISTINCT(article_id), next_station FROM process_time_table "
                    "WHERE next_station!=(?) ORDER BY next_station", ("Kunde",))
next_stations = prod_cursor.fetchall()
print(str(next_stations))

# data_frame = pd.read_sql(sql=prod_cursor.fetchall(), con=SQLITE3_HOST)
dataframe_logs = pd.DataFrame(table)
dataframe_stations_await = pd.DataFrame(next_stations)

# figure = px.bar(data_frame, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children="Hello Dash"),
    html.Div([
        html.H1("Aktivitäten: "),
        generate_table(dataframe_logs),
        #generate_table(dataframe2)
        html.H1("Stationen warten auf Artikel: "),
        generate_stations_await(dataframe_stations_await)
    ])
])

production_connection.close()

if __name__ == "__main__":
    app.run_server(debug=True)
