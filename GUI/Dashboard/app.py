import pandas as pd
from dash import Dash, html, dcc, dash_table
import sqlite3
import sqlalchemy
import time
import plotly.express as px

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"
table_head = ("production number", "article id", "order id",
              "station\t", "next station\t", "last station\t",
              "ID", "process end")
table_head_stations = ("Artikel-ID: ", "Station: ")

print("Baue Produktions-Datenbankverbindung auf....")
production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbankverbindung steht!")
prod_cursor = production_connection.cursor()


def generate_activities(data_frame, max_rows=100):
    return html.Table(className="mbox", children=[
        html.Thead(
            html.Tr([html.Th(table_head[col]) for col in data_frame.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
            ]) for i in range(min(len(data_frame), max_rows))
        ])
    ])


def generate_stations_await(data_frame, max_rows=10):
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

SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id), next_station FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY next_station ASC"

# data_frame = pd.read_sql(sql=prod_cursor.fetchall(), con=SQLITE3_HOST)
df = pd.read_sql(SQL_QUERY_PTT_1, production_connection)

df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

# figure = px.bar(data_frame, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children="Workflow Dashboard"),
    html.Div(children=[
        html.H2("Letzte Aktivitäten: "),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            fixed_rows={"headers": True},
            style_table={"height": 200,
                         "width": 1100,
                         "border-color": "black",
                         "border-style": "solid"},
            style_cell={"width": "10%",
                        "text-align": "center"}
        ),
        html.H2("Stationen warten auf Artikel: "),
        dash_table.DataTable(
            data=df_stations_await.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df_stations_await.columns],
            style_table={
                "width": 200,
                "border-color": "black",
                "border-style": "solid"
                },
            style_cell={
                "width": "50%",
                "text-align": "center"
                }
        )
    ])
])

production_connection.close()
print("Datenbankverbindung beendet!")

if __name__ == "__main__":
    app.run_server(debug=True)
