import math
from datetime import datetime
import plotly.io as pio
import pandas as pd
from dash import Dash, html, dcc, dash_table
import sqlite3
import sqlalchemy
import time
import plotly.express as px

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

print("Baue Produktions-Datenbankverbindung auf....")
production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbankverbindung steht!")
prod_cursor = production_connection.cursor()

app = Dash(__name__)

SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id), next_station FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY next_station ASC"

df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

prod_cursor.execute("SELECT * FROM process_time_table")
times = prod_cursor.fetchall()
print(len(times))

list_x = []
list_y = []
counter = []
for x in range(0, len(times)):
    counter.append(0)

for x in range(0, len(times)):
    if int(times[x][3]) in list_x:
        for y in range(0, len(list_x)):
            time_difference = datetime.strptime(times[x][7], "%d.%m.%Y %S:%M:%H") - \
                              datetime.strptime(times[x][6], "%d.%m.%Y %S:%M:%H")
            list_y[y] += int(time_difference.seconds / 60)
    else:
        list_x.append(int(times[x][3]))
        time_difference = datetime.strptime(times[x][7], "%d.%m.%Y %S:%M:%H") -\
                          datetime.strptime(times[x][6], "%d.%m.%Y %S:%M:%H")
        list_y.append(int(time_difference.seconds/60))

for x in range(0, len(times)):
    if int(times[x][3]) in list_x:
        counter[int(times[x][3])] += 1

for x in range(0, len(list_y)):
    list_y[x] /= counter[list_x[x]]
    list_y[x] = math.ceil(list_y[x])
print(list_x)
print(list_y)
print(counter)

#figure = px.bar(data_frame, x="Fruit", y="list_y" barmode="group")
fig = dict({
    "data": [{"type": "bar",
              "x": list_x,
              "y": list_y}],
    "layout": {"title": {"text": "A Figure Specified By Python Dictionary"}}
})
print(fig)

app.layout = html.Div(children=[
    html.H1(children="Workflow Dashboard"),
    html.Div(children=[
        html.H2("Letzte Aktivitäten: "),
        dash_table.DataTable(
            data=df_logs.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df_logs.columns],
            fixed_rows={"headers": True},
            style_table={
                "height": 200,
                "width": "50%",
                "border-color": "black",
                "border-style": "solid"},
            style_cell={
                "width": "10%",
                "text-align": "center"}
        )
    ]),
    html.Div(children=[
        html.H3("Stationen warten auf Artikel: "),
        dash_table.DataTable(
            data=df_stations_await.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df_stations_await.columns],
            style_table={
                "display": "inline-block",
                "width": 200,
                "border-color": "black",
                "border-style": "solid"
                },
            style_cell={
                "width": "50%",
                "text-align": "center"
                }
        )
    ]),
    html.Div(children=[
        dcc.Graph(figure=fig)
    ])
])
print(fig)
production_connection.close()
print("Datenbankverbindung beendet!")

if __name__ == "__main__":
    app.run_server(debug=True)
