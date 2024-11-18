from dash import html, dcc
import numpy as np
import fonctions as fct

# Charger le mesh
mesh_path = 'D:/Callisto/repo/Neuro-Mesh/data/mesh.gii'
texture_path = 'D:/Callisto/repo/Neuro-Mesh/data/Kmean.gii'
mesh = fct.load_mesh(mesh_path)
vertices = mesh.vertices
faces = mesh.faces

# Charger la texture (si fournie)
scalars = fct.read_gii_file(texture_path)

# Définir l'intervalle min et max par défaut des scalaires si disponibles
color_min_default, color_max_default = (np.min(scalars), np.max(scalars)) if scalars is not None else (0, 1)

# Layout pour la page 1
layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "backgroundColor": "#ffffff",
        "padding": "20px",
        "height": "calc(100vh - 60px)",  # Ajuste pour prendre tout l'espace sous la barre de navigation
        "boxSizing": "border-box",
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
                    "Visualisation de maillage 3D avec colormap interactive",
                    style={"margin": "0", "fontWeight": "bold", "fontSize": "28px"},
                ),
            ],
        ),

        # Contenu principal
        html.Div(
            style={
                "display": "flex",
                "flexGrow": 1,
                "width": "100%",
                "gap": "20px",
            },
            children=[
                # Panneau gauche : Options
                html.Div(
                    style={
                        "flex": "1",  # Équilibrer la largeur avec flex
                        "backgroundColor": "#f9f9f9",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "20px",
                    },
                    children=[
                        html.Label(
                            "Sélectionner le type de colormap",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Dropdown(
                            id='colormap-type-dropdown',
                            options=[
                                {'label': 'Sequential', 'value': 'sequential'},
                                {'label': 'Diverging', 'value': 'diverging'},
                                {'label': 'Cyclical', 'value': 'cyclical'}
                            ],
                            value='sequential',
                            clearable=False,
                            style={"marginBottom": "10px"},
                        ),
                        html.Label(
                            "Sélectionner une colormap",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Dropdown(
                            id='colormap-dropdown',
                            options=[{'label': cmap, 'value': cmap} for cmap in fct.get_colorscale_names('sequential')],
                            value='Viridis',
                            clearable=False,
                            style={"marginBottom": "10px"},
                        ),
                        html.Label(
                            "Afficher les isolignes",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Checklist(
                            id='toggle-contours',
                            options=[{'label': 'Oui', 'value': 'on'}],
                            value=[],
                            inline=True,
                            style={"marginBottom": "10px"},
                        ),
                        html.Label(
                            "Activer traits noirs",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Checklist(
                            id='toggle-black-intervals',
                            options=[{'label': 'Oui', 'value': 'on'}],
                            value=[],
                            inline=True,
                            style={"marginBottom": "10px"},
                        ),
                        html.Label(
                            "Centrer la colormap sur 0",
                            style={"fontWeight": "bold", "fontSize": "16px"},
                        ),
                        dcc.Checklist(
                            id='toggle-center-colormap',
                            options=[{'label': 'Oui', 'value': 'on'}],
                            value=[],
                            inline=True,
                            style={"marginBottom": "10px"},
                        ),
                    ],
                ),

                # Zone centrale : Visualisation
                html.Div(
                    style={
                        "flex": "2",  # Prend plus d'espace
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                    children=[
                        dcc.Graph(id='3d-mesh', style={"width": "100%", "height": "100%"}),
                    ],
                ),

                # Panneau droit : Slider
                html.Div(
                    style={
                        "flex": "1",  # Équilibrer la largeur avec flex
                        "backgroundColor": "#f9f9f9",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                    children=[
                        html.Label(
                            "Ajuster la plage de valeurs",
                            style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "20px"},
                        ),
                        html.Div(
                            style={
                                "width": "100%",
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                            children=[
                                dcc.RangeSlider(
                                    id='range-slider',
                                    min=color_min_default,
                                    max=color_max_default,
                                    step=0.01,
                                    value=[color_min_default, color_max_default],
                                    marks=fct.create_slider_marks(color_min_default, color_max_default),
                                    vertical=True,
                                    verticalHeight=500,
                                    tooltip={"placement": "right", "always_visible": True},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
