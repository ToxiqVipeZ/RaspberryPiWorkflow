import math
from datetime import datetime
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
import sqlite3
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.express as px

TIME_LIMIT = 11


def __init__(*args):
    TIME_LIMIT = args[0]


def stations_time_fig(data_table, mode):
    """
    This method calculates the time, a station needs, to proceed trough a workflow.
    It also serves other functions, determined by the mode parameter.
    :param data_table: List of data, acquired from the database
    :param mode: String Options: "station-times-bar", "", ""
    :return: returns a figure of the given data, the type of figure is determined by mode parameter
    """
    list_x = []
    list_y = []
    counter = []

    for x in range(0, len(data_table)):
        counter.append(0)

    # figure = px.bar(data_frame, x="Fruit", y="list_y" barmode="group")

    if mode == "station-times-bar":
        for x in range(0, len(data_table)):
            if int(data_table[x][3]) in list_x:
                for y in range(0, len(list_x)):
                    if data_table[x][7] != None:
                        time_difference = datetime.strptime(data_table[x][7], "%d.%m.%Y %S:%M:%H") - \
                                          datetime.strptime(data_table[x][6], "%d.%m.%Y %S:%M:%H")
                        list_y[y] += int(time_difference.seconds / 60)
            else:
                if data_table[x][7] != None:
                    list_x.append(int(data_table[x][3]))
                    time_difference = datetime.strptime(data_table[x][7], "%d.%m.%Y %S:%M:%H") - \
                                      datetime.strptime(data_table[x][6], "%d.%m.%Y %S:%M:%H")
                    list_y.append(int(time_difference.seconds / 60))

        for x in range(0, len(data_table)):
            if int(data_table[x][3]) in list_x:
                counter[int(data_table[x][3])] += 1

        for x in range(0, len(list_y)):
            list_y[x] /= counter[list_x[x]]
            list_y[x] = math.ceil(list_y[x])

        fig_station_times = go.Figure(
            data=[go.Bar(x=list_x, y=list_y)],
            layout=go.Layout(
                title=go.layout.Title(text="x = Stationen ; y = durchschnittliche Bearbeitungsdauer",
                                      font={"family": "Arial Black"}, y=0.82),
                showlegend=True
            )
        )

        fig_station_times.add_trace(go.Scatter(
            x=[0, int(graph_length) + 1],
            y=[TIME_LIMIT, TIME_LIMIT],
            mode="lines",
            line=go.scatter.Line(color="red"),
            showlegend=True
        ))

        return fig_station_times

    if mode == "placeholder":
        fig = dict({
            "data": [{"type": "bar",
                      "x": list_x,
                      "y": list_y}],
            "layout":
                {"title": {"text": "x = Stationen, y = Bearbeitungszeit"}, "title_font": "Arial Black"},
        })
        load_figure_template()
        return fig


SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbase connected.")
prod_cursor = production_connection.cursor()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dataquery's for data frames
SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table WHERE next_station!=\"Kunde\"" \
                  " ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id), next_station FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"

# Dataframes
df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

# full process-time-table (ptt_table) query
prod_cursor.execute("SELECT * FROM process_time_table")
ptt_table = prod_cursor.fetchall()
print("Amount of process time table Entry's: " + str(len(ptt_table)))

prod_cursor.execute("SELECT MAX(last_station) FROM process_time_table")
graph_length = prod_cursor.fetchone()[0]

figure_station_times = stations_time_fig(ptt_table, "station-times-bar")
some_value = None
# main-layout definition:
app.layout = html.Div(children=[
    dbc.Row(style={"margin": 5, "margin-top": 10}, justify="center", children=[
        dbc.Col(children=[html.H3(className="text-center", style={"text-decoration": "underline"},
                                  children="Workflow Dashboard")])]),

    dbc.Row(style={"height": "20%", "margin": 5, "margin-top": 0}, children=[
        dbc.Col(width=8, children=html.Div(children=[
            html.H5("Letzte Aktivitäten: "),
            dash_table.DataTable(
                id="activity_log",
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
                id="next_station_log",
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
        dbc.Col(html.Div(id='my_cards', children=[]))
    ]),
    dbc.Row(style={"height": 450, "margin": 5}, children=[
        dbc.Col(width=12, children=html.Div(children=[
            dcc.Graph(id="graph_update", figure={})
        ]))  # ,
        #    dbc.Col(width=2, style={"margin-top": 200}, children=[
        #        dcc.Input(
        #            id="input_time_limit".format("number"),
        #            type="number",
        #            placeholder="enter time limit".format("number")
        #        ),
        #        html.Div(id="return_input_time_limit")
        #    ])
    ]),
    dcc.Interval(interval=3 * 1000, n_intervals=0, id="refresh")
])
cards_made = []

@app.callback(
    Output("my_cards", "children"),
    [Input("refresh", "n_intervals")],
    State("my_cards", "children")
)
def make_cards(n_intervals, children):
    """Makes cards for each id"""
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    prod_cursor.execute("SELECT station, process_start, article_id"
                        " FROM process_time_table WHERE process_end IS (?)", (None,))
    p_end_empty = prod_cursor.fetchall()

    if not p_end_empty:
        raise PreventUpdate

    stations = [p_end_empty[x][0] for x in range(0, len(p_end_empty))]
    values = [p_end_empty[x][1] for x in range(0, len(p_end_empty))]
    article_id = [p_end_empty[x][2][:-3] for x in range(0, len(p_end_empty))]
    times = 0

    for x in range(0, len(stations)):
        prod_cursor.execute("SELECT procedure FROM article_procedure_table WHERE article_id=(?)",
                            (article_id[x],))
        procedure = prod_cursor.fetchone()[0]
        prod_cursor.execute("SELECT stations, times FROM workflow_planner_table WHERE workflow_procedure=(?)",
                            (procedure,))
        station_ref, time = prod_cursor.fetchone()
        station_ref = station_ref.split(";")
        times = time.split(";")
        print("time " + str(times))
        print("stations " + str(stations))

        # print(str(children.index("id")))
        children_ids = []

        #for item in children:
        #    if item == "id":
        #        children_ids.append(item)

        # children_ids = [x["id"] for x in children]
        #print(str(children_ids))
    print("%card%" in children)
    for x in range(0, len(stations)):
        index = station_ref.index(stations[x])
        station_name = "Station: " + stations[x]
        station_time = "Timelimit: " + times[index]
        # contained_child = False
        # for y in range(0, len(children_ids)):
        # if "card_" + stations[x] == children_ids[y]:
        # contained_child = True
        # if not contained_child:

        for item in cards_made:
            if item == "Div":
                print("poooop")

        if "card_" + stations[x] not in cards_made:
            my_card = html.Div(id="test", children=dbc.Card(id="card_" + stations[x], children=[
                station_name,
                dbc.CardBody(station_time)
            ], className="text-center"))
            cards_made.append(my_card)
            children.append(my_card)
    print("mycard: " + str(my_card))
    print(cards_made)

    return children


@app.callback(
    Output(component_id="station_activity", component_property="label"),
    Input(component_id="refresh", component_property="n_intervals")
)
def update_gauges(n_intervals):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()
    prod_cursor.execute("SELECT station, process_start FROM process_time_table WHERE process_end IS (?)", (None,))
    p_end_empty = prod_cursor.fetchone()
    print("test----x: " + str(p_end_empty))

    production_connection.close()
    return p_end_empty[0]


def call_database():
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    return production_connection, prod_cursor


@app.callback(
    Output(component_id="activity_log", component_property="data"),
    Input(component_id="refresh", component_property="n_intervals")
)
def update_activity_log(n_intervals):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)

    production_connection.close()

    return df_logs.to_dict("records")


@app.callback(
    Output(component_id="next_station_log", component_property="data"),
    Input(component_id="refresh", component_property="n_intervals")
)
def update_next_station(n_intervals):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

    production_connection.close()
    return df_stations_await.to_dict("records")


@app.callback(
    Output(component_id="graph_update", component_property="figure"),
    [Input(component_id="refresh", component_property="n_intervals")]
)
def update(n_intervals):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    # full process-time-table (ptt_table) query
    prod_cursor.execute("SELECT * FROM process_time_table")
    ptt_table = prod_cursor.fetchall()

    figure_station_times = stations_time_fig(ptt_table, "station-times-bar")

    production_connection.close()

    return figure_station_times


# Connection closing
production_connection.close()
print("Datenbase disconnected.")

# @app.callback(
#    Output("return_input_time_limit", "children"),
#    [Input("input_time_limit".format("number"), "value")]
# )
# def time_limit_setter(value):
#    figure_station_times.update_traces(selector=1, overwrite=True, y=[value, value])
#    return str(value)


if __name__ == "__main__":
    app.run_server(debug=True)
