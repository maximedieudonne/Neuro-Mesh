from dash import html, dcc

# Layout pour la page 2
layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "flex-start",
        "alignItems": "center",
        "height": "100%",
        "backgroundColor": "#ffffff",
        "padding": "20px",
    },
    children=[
        # Titre de la page
        html.Div(
            style={
                "textAlign": "center",
                "backgroundColor": "#3e4c6d",
                "padding": "15px",
                "color": "white",
                "borderRadius": "8px",
                "width": "100%",
                "marginBottom": "20px",
            },
            children=[
                html.H1(
                    "Interactive Colormap Builder",
                    style={"margin": "0", "fontWeight": "bold", "fontSize": "28px"},
                ),
                html.P("Advanced visualization and customization tool for colormaps"),
            ],
        ),

        # Contenu principal
        html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "gap": "20px",
                "width": "100%",
            },
            children=[
                # Panneau gauche : Options
                html.Div(
                    style={
                        "width": "40%",  # Augmenté pour plus de place
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "20px",  # Espacement entre les sections
                    },
                    children=[
                        # Section : Set Colormap Bounds
                        html.Div(
                            children=[
                                html.Label(
                                    "Set Colormap Bounds",
                                    style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"},
                                ),
                                html.Label("Min Colormap:", style={"fontSize": "14px"}),
                                dcc.Input(
                                    id="mincolormap",
                                    type="number",
                                    placeholder="Enter minimum colormap value",
                                    value=0,
                                    style={"width": "100%", "padding": "5px", "fontSize": "14px"},
                                ),
                                html.Label("Max Colormap:", style={"fontSize": "14px", "marginTop": "10px"}),
                                dcc.Input(
                                    id="maxcolormap",
                                    type="number",
                                    placeholder="Enter maximum colormap value",
                                    value=100,
                                    style={"width": "100%", "padding": "5px", "fontSize": "14px"},
                                ),
                                html.Button(
                                    "Apply Bounds",
                                    id="apply-bounds-btn",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "15px",
                                        "padding": "10px 15px",
                                        "fontSize": "14px",
                                        "backgroundColor": "#3e4c6d",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                        ),

                        # Section : Background Color
                        html.Div(
                            children=[
                                html.Label(
                                    "Background Color",
                                    style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"},
                                ),
                                dcc.Dropdown(
                                    id="background-color-dropdown",
                                    options=[
                                        {"label": "White", "value": "white"},
                                        {"label": "Black", "value": "black"},
                                        {"label": "Gray", "value": "gray"},
                                        {"label": "Light Blue", "value": "lightblue"},
                                        {"label": "Light Green", "value": "lightgreen"},
                                    ],
                                    value="white",
                                    style={"marginTop": "10px", "padding": "5px", "fontSize": "14px"},
                                ),
                            ],
                        ),

                        # Section : Add Color Range
                        html.Div(
                            children=[
                                html.Label(
                                    "Add Color Range",
                                    style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"},
                                ),
                                html.Label("Select Color:", style={"fontSize": "14px"}),
                                dcc.Dropdown(
                                    id="color-dropdown",
                                    options=[
                                        {"label": c.title(), "value": c}
                                        for c in [
                                            "red",
                                            "blue",
                                            "green",
                                            "orange",
                                            "purple",
                                            "yellow",
                                            "cyan",
                                            "magenta",
                                            "gray",
                                            "brown",
                                        ]
                                    ],
                                    placeholder="Select a color",
                                    style={"marginTop": "5px", "padding": "5px", "fontSize": "14px"},
                                ),
                                html.Label("Minimum Range:", style={"fontSize": "14px", "marginTop": "10px"}),
                                dcc.Input(
                                    id="min-range",
                                    type="number",
                                    placeholder="Enter min range",
                                    style={"width": "100%", "padding": "5px", "fontSize": "14px"},
                                ),
                                html.Label("Maximum Range:", style={"fontSize": "14px", "marginTop": "10px"}),
                                dcc.Input(
                                    id="max-range",
                                    type="number",
                                    placeholder="Enter max range",
                                    style={"width": "100%", "padding": "5px", "fontSize": "14px"},
                                ),
                                html.Button(
                                    "Add Color",
                                    id="add-color-btn",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "15px",
                                        "padding": "10px 15px",
                                        "fontSize": "14px",
                                        "backgroundColor": "#3e4c6d",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                        ),

                        # Section : Save and Load
                        html.Div(
                            children=[
                                html.Label(
                                    "Save & Load Colormaps",
                                    style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"},
                                ),
                                html.Button(
                                    "Save Colormap",
                                    id="save-colormap-btn",
                                    n_clicks=0,
                                    style={
                                        "padding": "10px 15px",
                                        "fontSize": "14px",
                                        "backgroundColor": "#3e4c6d",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                        "marginRight": "10px",
                                    },
                                ),
                                html.Span(
                                    id="save-status",
                                    style={"fontSize": "14px", "color": "green", "marginTop": "10px"},
                                ),
                                html.Div(
                                    style={"marginTop": "15px"},
                                    children=[
                                        html.Label("My Colormaps:", style={"fontSize": "14px"}),
                                        dcc.Dropdown(
                                            id="colormap-dropdown",
                                            placeholder="Select a colormap to load",
                                            style={"marginTop": "5px", "padding": "5px", "fontSize": "14px"},
                                        ),
                                    ],
                                ),
                                html.Button(
                                    "Reset Colormap",
                                    id="reset-colormap-btn",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "15px",
                                        "padding": "10px 15px",
                                        "fontSize": "14px",
                                        "backgroundColor": "#d9534f",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "4px",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),

                # Panneau droit : Visualisation
                html.Div(
                    style={
                        "width": "60%",  # Réduction pour équilibrer avec les options
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                    },
                    children=[
                        html.Label(
                            "Colormap Visualization",
                            style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "20px"},
                        ),
                        dcc.Graph(id="colormap-visual"),
                        html.Div(
                            id="color-info",
                            style={"marginTop": "20px", "fontSize": "14px", "lineHeight": "1.5", "color": "#333"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)
