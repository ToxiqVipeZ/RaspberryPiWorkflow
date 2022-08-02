from dash import dash, dcc, html, dash_table, callback_context
from dash.dependencies import Output, Input, State, MATCH
import math
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from datetime import datetime

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

production_connection = sqlite3.connect(SQLITE3_HOST)
prod_cursor = production_connection.cursor()

# Dataquery's for data frames
SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table WHERE next_station!=\"Kunde\"" \
                  " ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id) AS ArtikelID, station AS Push, next_station AS Pull" \
                  " FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"
SQL_QUERY_PTT_5 = "SELECT DISTINCT(article_id) AS ArtikelID, station AS Push, next_station AS Pull, process_end AS Checkout " \
                  "FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\"" \
                  "AND process_end!=\"None\" ORDER BY ROWID DESC"

df_stations_await_plus = pd.read_sql(SQL_QUERY_PTT_5, production_connection)
print(df_stations_await_plus)
# Dataframes
df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)

df_logs_columns = ["ProzessID", "ArtikelID", "BestellID", "Station",
                   "Nächste Station", "Endstation", "Startzeit", "Endzeit"]
df_stations_await_plus_columns = ["ArtikelID", "Push", "Pull", "Wartezeit"]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, ".assets/stylesheet.css"],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1"}]
                )

app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.H2(children="Workstation Dashboard",
                    className="text-center text-primary",
                    style={"margin-top": 20,
                           "margin-bottom": 20,
                           "border-color": "blue",
                           "border-style": "outset",
                           "border-width": "4px"
                           }
                    ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(style={"display": "block"}, width=3, align="left", children=html.Div(children=[
            html.H5(children=["Stationen erwarten: "], className="text-primary", style={"margin-top": 10}),
            dash_table.DataTable(
                id="next_station_log",
                data=df_stations_await_plus.to_dict("records"),
                columns=[{
                    'name': col,
                    'id': df_stations_await_plus.columns[idx]
                } for (idx, col) in enumerate(df_stations_await_plus_columns)],
                fixed_rows={"headers": True},
                style_header={
                    "fontWeight": "bold",
                    "border": "2px solid black",
                    "border-bottom": "2px solid blue"
                },
                style_table={
                    "height": 400,
                    "border-color": "blue",
                    "border-style": "outset",
                    "border-width": "4px"
                },
                style_cell={
                    "width": "10%",
                    "text-align": "center",
                    "fontWeight": "bold",
                    "font-size": 14,
                    "background-color": "black",
                    "font-style": "Open Sans"
                },
                style_as_list_view=True
            ),
        ])),
        dbc.Col(
            style={"display": "inline-block", "padding-bottom": 30},
            children=[
                html.H5(children=["Aktive Stationen: "],
                        style={"display": "block", "margin-top": 10, "margin-bottom": -2},
                        className="text-primary"),
                html.Div(
                    style={"display": "inline-block", "height": 400},
                    id="card-container",
                    children=[]
                )
            ], width=9
        ),
    ]),
    dbc.Row(children=[
        dbc.Col(children=[
            html.H5(children=["Logs: "], className="text-primary", style={"margin-top": 10}),
            dash_table.DataTable(
                id="activity_log",
                data=df_logs.to_dict("records"),
                columns=[{
                    'name': col,
                    'id': df_logs.columns[idx]
                } for (idx, col) in enumerate(df_logs_columns)],
                fixed_rows={"headers": True},
                style_header={
                    "fontWeight": "bold",
                    "border": "2px solid black",
                    "border-bottom": "2px solid blue"
                },
                style_table={
                    "height": 200,
                    "border-color": "blue",
                    "border-style": "outset",
                    "border-width": "4px"
                },
                style_cell={
                    "width": "10%",
                    "text-align": "center",
                    "fontWeight": "bold",
                    "font-size": 14,
                    "background-color": "black",
                    "font-style": "Open Sans"
                },
                style_as_list_view=True
            )
        ], width=8),
        dbc.Col(width=3, children=[
            html.H5(children=["Fehlermeldungen: "], className="text-primary", style={"margin-top": 10}),
            dbc.Card(style={"border-color": "blue", "border-style": "outset", "border-width": "4px"},
                     children=[dbc.CardHeader("Station 01"),
                               dbc.CardBody("Fehler: XYZ"),
                               dbc.CardFooter("Betroffene Stationen: 02, 03, 05")])
        ])
    ]),
    dbc.Row(dbc.Col()),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="add-card"),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="add-time"),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="puffer_time_check")
], style={"margin": 20})

production_connection.close()


@app.callback(
    Output(component_id="next_station_log", component_property="data"),
    Input(component_id="puffer_time_check", component_property="n_intervals")
)
def stations_puffer_time(n_intervals):
    production_connection = sqlite3.connect(SQLITE3_HOST)

    df_stations_await_plus = pd.read_sql(SQL_QUERY_PTT_5, production_connection)

    for x in range(0, len(df_stations_await_plus)):
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        time_now = datetime.strptime(now, "%d.%m.%Y %H:%M:%S")
        checkout = datetime.strptime(df_stations_await_plus["Checkout"][x], "%d.%m.%Y %H:%M:%S")
        difference = (time_now - checkout)

        df_stations_await_plus["Checkout"][x] = str(difference)

    production_connection.close()
    # print(df_stations_await_plus.to_dict("records"))
    return df_stations_await_plus.to_dict("records")


@app.callback(
    Output("card-container", "children"),
    [Input("add-card", "n_intervals")],
    [State("card-container", "children")],
    blocking=True
)
def display_cards(n_intervals, div_children):
    """
    This method gets called every 0,5 seconds.
    This method creates cards depending on entry's inside the "process_time_table" - database table.
    If a entry has no "check-out"-time, them it means a station is working, therefore a card will be created.
    The method gives back a card as children to the card-container div.
    """
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cursor = production_connection.cursor()

    SQL_QUERY_PTT_3 = "SELECT station, process_start, article_id " \
                      "FROM process_time_table WHERE process_end IS NULL"

    card_df = pd.read_sql(SQL_QUERY_PTT_3, production_connection)
    card_df = card_df.sort_values(by="station")
    card_df = card_df.reset_index(drop=True)

    n_intervals = n_intervals % len(card_df)
    station_nr = card_df.get("station")[n_intervals]
    if div_children is not None:
        if len(div_children) < len(card_df):
            if n_intervals in range(0, len(card_df)):
                new_card = html.Div(
                    style={"width": 210, "height": 180,
                           "margin": 10, "margin-left": 0, "textAlign": "center",
                           "display": "inline-block", "verticalAlign": "top",
                           "horizontalAlign": "right"},
                    children=[
                        dbc.Card(
                            id={
                                "type": "dynamic-cards",
                                "index": station_nr
                            },
                            children=[
                                dbc.CardHeader("Station: " + station_nr),
                                dbc.CardBody(
                                    id={
                                        "type": "dynamic-cards-text",
                                        "index": station_nr
                                    },
                                    children=[],
                                    className="text-white"
                                ),
                            ],
                            style={"border-color": "blue",
                                   "border-style": "outset",
                                   "border-width": "4px"
                                   },
                            className="text-white"
                        )
                    ]
                )
                div_children.append(new_card)
                production_connection.close()
                return div_children
            else:
                production_connection.close()
                return dash.no_update
        else:
            production_connection.close()
            return dash.no_update
    else:
        production_connection.close()
        return dash.no_update


@app.callback(
    Output({"type": "dynamic-cards-text", "index": MATCH}, "children"),
    [Input("add-time", "n_intervals")],
    [State({"type": "dynamic-cards-text", "index": MATCH}, "children")],
    blocking=True
)
def display_time(n_intervals, children):
    """
    This method calculates and displays the time inside a Stationcard.
    The time and the time-limit get passed as children to the card-object.
    This method gets called every 0.5 seconds to display the time correctly.
    """
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cur = production_connection.cursor()

    SQL_QUERY_PTT_3 = "SELECT station, process_start, article_id FROM process_time_table WHERE process_end IS NULL"

    children_index = str(callback_context.outputs_grouping)
    children_index = children_index.split("\'index\': \'")[1][:2]
    card_df = pd.read_sql(SQL_QUERY_PTT_3, production_connection)
    card_df = card_df.sort_values(by="station")
    card_df = card_df.reset_index(drop=True)

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    time_now = datetime.strptime(now, "%d.%m.%Y %H:%M:%S")

    for x in range(0, len(card_df)):
        if card_df["station"][x] == children_index:
            check_in = card_df["process_start"][x]
            article_id = card_df["article_id"][x]

            prod_cur.execute("SELECT procedure FROM article_procedure_table "
                             "WHERE article_id=(?)", (article_id[:-3],))
            procedure = prod_cur.fetchone()[0]

            prod_cur.execute("SELECT stations, times FROM workflow_planner_table "
                             "WHERE workflow_procedure=(?)", (procedure,))
            time_limit = prod_cur.fetchone()
            time_limit_stations = time_limit[0].split(";")
            time_limit_times = time_limit[1].split(";")
            for y in range(0, len(time_limit[0])):
                if children_index == time_limit_stations[y]:
                    time_limit_station = int(time_limit_times[y])
                    # time_limit_station = datetime.strptime(time_limit_station, "%S")
                    time_check_in = datetime.strptime(check_in, "%d.%m.%Y %H:%M:%S")
                    difference = time_now - time_check_in
                    body_child = str(difference)
                    difference_in_sec = int(difference.total_seconds())
                    minus_time_limit = time_limit_station - difference_in_sec
                    color = "grey"
                    textColor = "text-white"
                    if minus_time_limit < 0:
                        color = "yellow"
                        textColor = "text-black"
                        if minus_time_limit <= -20:
                            color = "darkred"
                            textColor = "text-white"
                            if minus_time_limit <= -200001:
                                minus_time_limit = math.ceil(minus_time_limit / 10000)
                    elif minus_time_limit > 0:
                        color = "green"
                        textColor = "text-white"
                    minus_time_limit = "Zeitlimit: " + str(minus_time_limit) + "\n"
                    footer_child = dbc.CardFooter(
                        children=[minus_time_limit, str(article_id)],
                        style={
                            "margin-top": "10px",
                            "border-style": "outset",
                            "border-color": "darkblue",
                            "border-radius": "10px",
                            "display": "inline-block",
                            "background-color": color
                        },
                        className=textColor
                    )
                    return [body_child, footer_child]


if __name__ == "__main__":
    app.run_server(debug=True)
