import math
from datetime import datetime

import dash.dependencies
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
import sqlite3
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH
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
    dbc.Row(id="card_row", style={"display": "inline-block", "height": 300, "margin": 10}, children=[
        dbc.Col(style={"display": "inline-block"}, id='my_cards', children=[
            dbc.Card(
                id="card_container_01",

                style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                       "display": "inline-block", "verticalAlign": "top"},

                children=["Station: 01", dbc.CardBody(
                    children=[html.Div(id={"type": "card_time_text", "index": "card_01"},
                                       children=[]
                    )]
                )]
            ),
            dbc.Card(
                id="card_container_02",

                style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                       "display": "inline-block", "verticalAlign": "top"},

                children=["Station: 02", dbc.CardBody(
                    children=[html.Div(id={"type": "card_time_text", "index": "card_02"},
                                       children=[]
                    )]
                )]
            ),
            dbc.Card(
                id="card_container_03",

                style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                       "display": "inline-block", "verticalAlign": "top"},

                children=["Station: 03", dbc.CardBody(
                    children=[html.Div(id={"type": "card_time_text", "index": "card_03"},
                                       children=[]
                    )]
                )]
            ),
            dbc.Card(
                id="card_container_04",

                style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                       "display": "inline-block", "verticalAlign": "top"},

                children=["Station: 04", dbc.CardBody(
                    children=[html.Div(id={"type": "card_time_text", "index": "card_04"},
                                       children=[]
                    )]
                )]
            ),
            dbc.Card(
                id="card_container_05",

                style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                       "display": "inline-block", "verticalAlign": "top"},

                children=["Station: 05", dbc.CardBody(
                    children=[html.Div(id={"type": "card_time_text", "index": "card_05"},
                                       children=[]
                )]
            )]
        )
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
    dcc.Interval(interval=3 * 1000, n_intervals=-1, id="refresh"),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="refresh_cards")
])
])

@app.callback(
    Output({"type": "card_time_text", "index": MATCH}, "children"),
    [Input("refresh_cards", "n_intervals")],
    State({"type": "card_time_text", "index": MATCH}, "id"),
    blocking=True
)
def display_time(n_intervals, children):
    try:
        SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
        # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

        production_connection = sqlite3.connect(SQLITE3_HOST)
        prod_cursor = production_connection.cursor()

        SQL_QUERY_PTT_3 = "SELECT station, process_start, article_id " \
                          "FROM process_time_table WHERE process_end IS NULL"
        child = str(children)
        child.split(",")
        station = child[42:44]
        card_text_df = pd.read_sql(SQL_QUERY_PTT_3, production_connection)
        card_text_df = card_text_df.sort_values(by="station")
        card_text_df = card_text_df.reset_index(drop=True)
        print(card_text_df)
        x = 0

        for item in card_text_df.get("station"):
            if item == station:
                break
            x += 1

        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        check_in = card_text_df.get("process_start")[x]

        t1 = datetime.strptime(now, "%d.%m.%Y %H:%M:%S")
        t2 = datetime.strptime(check_in, "%d.%m.%Y %H:%M:%S")

        difference = str(t1 - t2)
        print("update" + str(children))

        # print(str(html.Div(id={"type": "card_time_text", "index": "card_" + card_text_df.get("station")[x]}, children=[html.P([difference])])))

        return html.P(difference)
    except KeyError:
        pass


# print(str(children.index("id")))
# children_ids = []

# for item in children:
#    if item == "id":
#        children_ids.append(item)

# children_ids = [x["id"] for x in children]
# print(str(children_ids))


"""
@app.callback(
    Output("my_cards", "children"),
    [Input("refresh", "n_intervals")],
    State("my_cards", "children"),
    blocking=True
)
def make_cards(n_intervals, children):

    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    SQL_QUERY_PTT_3 = "SELECT station, process_start, article_id " \
                      "FROM process_time_table WHERE process_end IS NULL"

    card_df = pd.read_sql(SQL_QUERY_PTT_3, production_connection)
    card_df = card_df.sort_values(by="station")
    card_df = card_df.reset_index(drop=True)

    print(datetime.now())

    # print(card_df)
    # print(card_df.get("station")[1])

    # stations = [p_end_empty[x][0] for x in range(0, len(p_end_empty))]
    # values = [p_end_empty[x][1] for x in range(0, len(p_end_empty))]
    # article_id = [p_end_empty[x][2][:-3] for x in range(0, len(p_end_empty))]
    # times = 0
    child_arr = children

    if len(children) < len(card_df):
        for x in range(0, len(card_df)):

            article_id = card_df.get("article_id")[x]
            article_id = article_id[:-3]
            prod_cursor.execute("SELECT procedure FROM article_procedure_table WHERE article_id=(?)",
                                (article_id,))
            procedure = prod_cursor.fetchone()[0]

            prod_cursor.execute("SELECT stations, times FROM workflow_planner_table WHERE workflow_procedure=(?)",
                                (procedure,))
            station_ref, time = prod_cursor.fetchone()
            station_ref = station_ref.split(";")
            times = time.split(";")
            stations_times_df = pd.DataFrame(data=([station_ref, times]))
            stations_times_df = stations_times_df.T
            stations_times_df.columns = ["stations", "times"]
            station = card_df.get("station")[x]

            # print(station + "< station station_ref >" + station_ref[x])
            # station_index = station_time.__pos__(station)
            # print(card_df)
            # print(station_ref)
            print("-----------------------")
            # print(len(children))
            print(len(card_df))
            # print(station_time)
            # print(str(station_index) + "iiiiiiiiiiiiiiiiiiiiiindex")
            # times_df = pd.DataFrame(data=times)
            # card_df[x] += times[x]
            # print("time " + str(times))

            # card_df = card_df.__set("times", times)
            # print(card_df)

            # for x in range(0, len(card_df)):
            # datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            # print(stations_times_df.get("times"))
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            check_in = card_df.get("process_start")[x]

            t1 = datetime.strptime(now, "%d.%m.%Y %H:%M:%S")
            t2 = datetime.strptime(check_in, "%d.%m.%Y %H:%M:%S")

            difference = str(t1 - t2)
            print("station: " + station)
            # print("now: " + str(t1) + " check in: " + str(t2) + "difference: " + str(difference))

            if ("id={'type': 'card_time_text', 'index': 'card_" + station + "'}") not in children:
                children.append(
                    dbc.Card(
                        id="card_container_" + station,

                        style={"width": 100, "height": 100, "margin-left": 10, "textAlign": "center",
                               "display": "inline-block", "verticalAlign": "top"},

                        children=["Station: " + station, dbc.CardBody(
                            children=[html.Div(id={"type": "card_time_text", "index": "card_" + station},
                                               children=[html.P([difference])])]
                        )]
                    )
                )
                print("0: " + str(children))

        # for items in child_arr:
        #    children.append(items)
        #    print("item = " + str(items))
        # print(str(child_arr))

    if len(children) == len(card_df):
        print("children full")

    return children



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
        fig_card = figure(
            data=[go.Box(children=dbc.Card(id="card_" + stations[x], children=[
                    station_name,
                    dbc.CardBody(station_time)
                    ], className="text-center"
                )
            )]
        )
        fig_card.to_dict()
        cards_made.append(fig_card)
        children.append(fig_card)

        #my_card = go.figure(id="test", children=dbc.Card(id="card_" + stations[x], children=[
        #    station_name,
        #    dbc.CardBody(station_time)
        #], className="text-center"))
        #my_card_dict = my_card.to_dict()
        #cards_made.append(my_card)
        #children.append(my_card)
        print("mycard: " + str(fig_card))
        print(cards_made)

# fig_station_times = go.Figure(
#    data=[go.Bar(x=list_x, y=list_y)],
#    layout=go.Layout(
#        title=go.layout.Title(text="x = Stationen ; y = durchschnittliche Bearbeitungsdauer",
#                              font={"family": "Arial Black"}, y=0.82),
#        showlegend=True
#    )
# )
"""


# @app.callback(
#    Output(component_id="station_activity", component_property="label"),
#    Input(component_id="refresh", component_property="n_intervals")
# )
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
