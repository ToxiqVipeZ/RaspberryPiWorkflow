from dash import dash, dcc, html, dash_table
from dash.dependencies import Output, Input, State, MATCH
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from datetime import datetime

SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
# SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

production_connection = sqlite3.connect(SQLITE3_HOST)
print("Datenbase connected.")
prod_cursor = production_connection.cursor()

# Dataquery's for data frames
SQL_QUERY_PTT_1 = "SELECT * FROM process_time_table WHERE next_station!=\"Kunde\"" \
                  " ORDER BY ROWID DESC"
SQL_QUERY_PTT_2 = "SELECT DISTINCT(article_id), next_station FROM process_time_table " \
                  "WHERE next_station!=\"Kunde\" ORDER BY ROWID DESC"


# Dataframes
df_logs = pd.read_sql(SQL_QUERY_PTT_1, production_connection)
df_stations_await = pd.read_sql(SQL_QUERY_PTT_2, production_connection)


print(df_logs)
print("-------------------")
print(df_stations_await)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1.0"}]
                )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Workstation Dashboard",
                    className="text-center text-primary, mb-4"),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            width=12,
            style={"display": "inline-block"},
            children=[
                html.Div(
                    id="card-container",
                    children=[]
                )
            ]
        )
    ]),
    dbc.Row([

    ]),
    dcc.Interval(interval=1 * 1000, n_intervals=0, id="add-card"),
    dcc.Interval(interval=1 * 500, n_intervals=0, id="add-time")
])

production_connection.close()


@app.callback(
    Output("card-container", "children"),
    [Input("add-card", "n_intervals")],
    [State("card-container", "children")]
)
def display_cards(n_intervals, div_children):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    print("Datenbase connected.")
    prod_cursor = production_connection.cursor()

    SQL_QUERY_PTT_3 = "SELECT station, process_start, article_id " \
                      "FROM process_time_table WHERE process_end IS NULL"

    card_df = pd.read_sql(SQL_QUERY_PTT_3, production_connection)
    card_df = card_df.sort_values(by="station")
    card_df = card_df.reset_index(drop=True)

    n_intervals = n_intervals % len(card_df)
    station_nr = card_df.get("station")[n_intervals]
    if div_children is not None:
        print(len(div_children))
        print(len(card_df))
        if len(div_children) < len(card_df):
            if n_intervals in range(0, len(card_df)):
                new_card = html.Div(
                    children=[
                        dbc.Card(
                            id={
                                "type": "dynamic-cards",
                                "index": station_nr
                            },

                            style={"width": 125, "height": 125, "margin-left": 10, "textAlign": "center",
                                   "display": "inline-block", "verticalAlign": "top"},

                            children=[
                                dbc.CardHeader("Station: " + station_nr),
                                dbc.CardBody(
                                    html.P(
                                        id={
                                            "type": "dynamic-cards-text",
                                            "index": station_nr
                                        },
                                        children=[]
                                    )
                                ),
                            ]
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
    [State({"type": "dynamic-cards-text", "index": MATCH}, "children")]
)
def display_time(n_intervals, children):
    SQLITE3_HOST = "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db"
    # SQLITE3_HOST = "//FILESERVER/ProductionDatabase/productionDatabase.db"

    production_connection = sqlite3.connect(SQLITE3_HOST)
    prod_cur = production_connection.cursor()

    prod_cur.execute("SELECT station, process_start, article_id FROM process_time_table WHERE process_end IS NULL")

    data = prod_cur.fetchall()
    data.sort("station")

    #card_df = pd.read_sql(SQL_QUERY_PTT_4, production_connection)
    #card_df = card_df.sort_values(by="station")
    #card_df = card_df.reset_index(drop=True)

    print(children)
    #child.split(",")
    #station = child[42:44]

    #index = data.index(station)

    #print(index)
    print(data)


    return children

if __name__ == "__main__":
    app.run_server(debug=True)
