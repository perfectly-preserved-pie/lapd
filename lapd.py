from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import uuid

external_stylesheets = [
    dbc.icons.BOOTSTRAP,
    dbc.icons.FONT_AWESOME,
    dbc.themes.DARKLY,
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css",
]

df = pd.read_excel('data/lapd.xlsx')

# Generate a unique ID for each row
df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

# Drop the Item# column
df = df.drop(columns=['Item#'])

# Drop any rows that don't have a description
df = df.dropna(subset=['Description'])

app = Dash(__name__, external_stylesheets=external_stylesheets)

def generate_column_definitions(dataframe: pd.DataFrame) -> list:
    """
    Generates AG-Grid column definitions from a pandas DataFrame, pinning the "Description" column
    to the left and hiding the "uuid" column.

    Args:
        dataframe: A pandas DataFrame to generate column definitions from.

    Returns:
        A list of dictionaries, each containing the configuration for a column.
    """
    column_defs = []
    for column in dataframe.columns:
        column_def = {
            "field": column,
            "minWidth": 150,
            "resizable": True,
            "sortable": True,
            "filter": True,
            "floatingFilter": True,
            "suppressMenu": True
        }
        # Pin the "Description" column to the left
        if column == "Description":
            column_def["pinned"] = "left"
        # Hide the "uuid" column
        if column == "uuid":
            column_def["hide"] = True
        
        column_defs.append(column_def)
    return column_defs

column_defs = generate_column_definitions(df)

app.layout = html.Div(
    style={'height': '100vh', 'width': '100vw'},  # This will make the div take the entire viewport
    children=[
        dag.AgGrid(
            id='grid',
            columnDefs=column_defs,
            rowData=df.to_dict('records'),
            style={
                'width': '100%',  # Makes the AgGrid component take the entire width of its parent
                'height': '100%',  # Makes the AgGrid component take the entire height of its parent
            },
        ),
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
