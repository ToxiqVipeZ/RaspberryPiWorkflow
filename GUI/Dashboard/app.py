import math
from datetime import datetime
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import sqlite3
import plotly.graph_objects as go
import plotly.express as px


def stations_time_fig(ptt_table, mode):
    list_x = []
    list_y = []
    counter = []
    for x in range(0, len(ptt_table)):
        counter.append(0)

    for x in range(0, len(ptt_table)):
        if int(ptt_table[x][3]) in list_x:
            for y in range(0, len(list_x)):
                time_difference = datetime.strptime(ptt_table[x][7], "%d.%m.%Y %S:%M:%H") - \
                                  datetime.strptime(ptt_table[x][6], "%d.%m.%Y %S:%M:%H")
                list_y[y] += int(time_difference.seconds / 60)
        else:
            list_x.append(int(ptt_table[x][3]))
            time_difference = datetime.strptime(ptt_table[x][7], "%d.%m.%Y %S:%M:%H") - \
                              datetime.strptime(ptt_table[x][6], "%d.%m.%Y %S:%M:%H")
            list_y.append(int(time_difference.seconds / 60))

    for x in range(0, len(ptt_table)):
        if int(ptt_table[x][3]) in list_x:
            counter[int(ptt_table[x][3])] += 1

    for x in range(0, len(list_y)):
        list_y[x] /= counter[list_x[x]]
        list_y[x] = math.ceil(list_y[x])

    # figure = px.bar(data_frame, x="Fruit", y="list_y" barmode="group")

    fig2 = go.Figure(
        data=[go.Bar(x=list_x, y=list_y)],
        layout=go.Layout(
            title=go.layout.Title(text="x = Stationen ; y = durchschnittliche Bearbeitungsdauer",
                                  font={"family": "Arial Black"}, y=0.82)
        )
    )


    fig = dict({
        "data": [{"type": "bar",
                  "x": list_x,
                  "y": list_y}],
        "layout":
            {"title": {"text": "x = Stationen, y = Bearbeitungszeit"}, "title_font": "Arial Black"},
    })
    fig.update()
    load_figure_template()
    return fig2


SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbase connected.")
prod_cursor = production_connection.cursor()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dataquery's for data frames
SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id), next_station FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"

# Dataframes
df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

# full process-time-table (ptt_table) query
prod_cursor.execute("SELECT * FROM process_time_table")
ptt_table = prod_cursor.fetchall()
print("Amount of process time table Entry's: " + str(len(ptt_table)))

# main-layout definition:
app.layout = html.Div(children=[
    dbc.Row(style={"margin": 5, "margin-top": 10}, justify="center", children=[
        dbc.Col(children=[html.H3(className="text-center", style={"text-decoration": "underline"},
                                  children="Workflow Dashboard")])]),

    dbc.Row(style={"height": "20%", "margin": 5, "margin-top": 0}, children=[
        dbc.Col(width=8, children=html.Div(children=[
            html.H5("Letzte Aktivitäten: "),
            dash_table.DataTable(
                data=df_logs.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_logs.columns],
                fixed_rows={"headers": True},
                style_table={
                    "height": 150,
                    "border-color": "black",
                    "border-style": "solid",
                    "border-width": 2
                },
                style_cell={
                    "width": "10%",
                    "text-align": "center",
                    "font-size": 12,
                    "font-style": "Open Sans"
                }
            )
        ])),
        dbc.Col(width=4, align="right", children=html.Div(children=[
            html.H5("Nächste Stationen: "),
            dash_table.DataTable(
                data=df_stations_await.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_stations_await.columns],
                fixed_rows={"headers": True},
                style_table={
                    "height": 150,
                    "border-color": "black",
                    "border-style": "solid",
                    "border-width": 2
                },
                style_cell={
                    "width": "50%",
                    "text-align": "center",
                    "font-size": 12
                }
            )
        ]))
    ]),
    # Platzhalter für weiteren Content:
    dbc.Row(style={"height": 300, "margin": 5}, children=[
        dbc.Col(

        ),
        dbc.Col(

        ),
        dbc.Col(

        )
    ]),

    dbc.Row(style={"height": 450, "margin": 5}, children=dbc.Col(children=html.Div(children=[
        dcc.Graph(figure=stations_time_fig(ptt_table, "graph"))
    ])))
    ])

# Connection closing
production_connection.close()
print("Datenbase disconnected.")

if __name__ == "__main__":
    app.run_server(debug=True)
