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

# Dataframes
df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)
df_stations_await_plus = pd.read_sql(SQL_QUERY_PTT_5, production_connection)

df_logs_columns = ["ProzessID", "ArtikelID", "BestellID", "Station",
                   "Weiter", "Endstation", "Startzeit", "Endzeit"]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, ".assets/stylesheet.css"],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1.0"}]
                )

app.layout = dbc.Container([
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
    dbc.Row(
        style={"display": "inline-block"
               },
        children=[
            html.H5(children=["Aktive Stationen: "], className="text-primary"),
            dbc.Col(
                style={"display": "inline-block", "padding-bottom": 30},
                children=[
                    html.Div(
                        style={"display": "inline-block"},
                        id="card-container",
                        children=[]
                    )
                ], width=12
            ),
        ]
    ),
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
                    "height": 150,
                    "border-color": "blue",
                    "border-style": "outset",
                    "border-width": "4px"
                },
                style_cell={
                    "width": "10%",
                    "text-align": "center",
                    "fontWeight": "bold",
                    "font-size": 12,
                    "background-color": "black",
                    "font-style": "Open Sans"
                },
                style_as_list_view=True
            )
        ], width=8),
        dbc.Col(width=4, align="right", children=html.Div(children=[
            html.H5(children=["Stationen erwarten: "], className="text-primary", style={"margin-top": 10}),
            dash_table.DataTable(
                id="next_station_log",
                data=df_stations_await.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_stations_await.columns],
                fixed_rows={"headers": True},
                style_header={
                    "fontWeight": "bold",
                    "border": "2px solid black",
                    "border-bottom": "2px solid blue"
                },
                style_table={
                    "height": 150,
                    "border-color": "blue",
                    "border-style": "outset",
                    "border-width": "4px"
                },
                style_cell={
                    "width": "10%",
                    "text-align": "center",
                    "fontWeight": "bold",
                    "font-size": 12,
                    "background-color": "black",
                    "font-style": "Open Sans"
                },
                style_as_list_view=True
            )
        ]))
    ]),
    dbc.Row(dbc.Col()),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="add-card"),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="add-time")
])

production_connection.close()

@app.callback(
    Output("next_station_log", "data"),
    [Input("add-card", "n_intervals")],
    blocking=True
)
def stations_puffer_time(n_intervals):
    for x in range(0, len(df_stations_await_plus["Checkout"])):
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        time_now = datetime.strptime(now, "%d.%m.%Y %H:%M:%S")
        check_out = str(df_stations_await_plus["Checkout"][x])
        time_now = now.total_seconds()
        time_check_out = time_check_out.total_seconds()

        difference = time_check_out - time_now
        difference_in_sec = int(difference.total_seconds())
        df_stations_await_plus["Checkout"][x] = str(difference)

    return df_stations_await_plus

@app.callback(
    Output("card-container", "children"),
    [Input("add-card", "n_intervals")],
    [State("card-container", "children")],
    blocking=True
)
def display_cards(n_intervals, div_children):
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
                    style={"width": 210, "height": 150, "margin": 10, "margin-left": 0, "textAlign": "center",
                           "display": "inline-block", "verticalAlign": "top", "horizontalAlign": "right"},
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
                                    children=[]
                                ),
                            ],
                            style={"border-color": "blue",
                                   "border-style": "outset",
                                   "border-width": "4px"}
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
                    if minus_time_limit < 0:
                        color = "yellow"
                        if minus_time_limit <= -20:
                            color = "red"
                            if minus_time_limit <= -200001:
                                minus_time_limit = math.ceil(minus_time_limit / 10000)
                    elif minus_time_limit > 0:
                        color = "green"

                    footer_child = dbc.CardFooter(
                        children=["time limit: " + str(minus_time_limit), "\n" + str(article_id)],
                        style={
                            "margin-top": "10px",
                            "border-style": "outset",
                            "border-color": "darkblue",
                            "border-radius": "10px",
                            "display": "inline-block",
                            "background-color": color
                        }
                    )
                    return [body_child, footer_child]


if __name__ == "__main__":
    app.run_server(debug=True)
