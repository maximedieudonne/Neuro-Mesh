from dash import html, dcc

# Layout pour la page 1
layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "flex-start",
        "alignItems": "center",
        "height": "100%",
        "backgroundColor": "#ffffff",
        "borderRadius": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
        "padding": "20px",
    },
    children=[
        html.H2("Page 1: Choose a Color", style={"marginBottom": "20px"}),
        html.Div(
            style={
                "width": "100%",
                "maxWidth": "400px",
                "textAlign": "center",
            },
            children=[
                dcc.Dropdown(
                    id='color-picker',
                    options=[
                        {'label': 'Red', 'value': 'red'},
                        {'label': 'Blue', 'value': 'blue'},
                        {'label': 'Green', 'value': 'green'},
                    ],
                    placeholder="Select a color",
                    style={
                        "marginBottom": "20px",
                        "padding": "10px",
                        "fontSize": "16px",
                    },
                ),
                html.Div(
                    id='color-output',
                    style={
                        "marginTop": "20px",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                    },
                ),
            ],
        ),
    ],
)
