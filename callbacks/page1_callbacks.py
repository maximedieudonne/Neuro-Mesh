from dash.dependencies import Input, Output, State
import fonctions as fct
import numpy as np
import json

def register_callbacks(app):
    # Chemins vers les fichiers de données
    mesh_path = 'D:/Callisto/repo/Neuro-Mesh/data/mesh.gii'
    texture_path = 'D:/Callisto/repo/Neuro-Mesh/data/Kmean.gii'

    # Charger le mesh
    mesh = fct.load_mesh(mesh_path)
    vertices = mesh.vertices
    faces = mesh.faces

    # Charger la texture (si disponible)
    scalars = fct.read_gii_file(texture_path) if texture_path else None

    # Valeurs par défaut pour les scalaires
    color_min_default, color_max_default = (np.min(scalars), np.max(scalars)) if scalars is not None else (0, 100)

    # Charger les colormaps enregistrées
    try:
        with open("saved_colormaps.json", "r") as file:
            saved_colormaps = json.load(file)
    except FileNotFoundError:
        saved_colormaps = {}

    @app.callback(
        Output('3d-mesh', 'figure'),
        [
            Input('range-slider', 'value'),
            Input('toggle-contours', 'value'),
            Input('toggle-black-intervals', 'value'),
            Input('colormap-dropdown', 'value'),
            Input('toggle-center-colormap', 'value'),
        ],
        [State('3d-mesh', 'relayoutData')]
    )
    def update_figure(value_range, toggle_contours, toggle_black_intervals, selected_colormap, center_colormap, relayout_data):
        min_value, max_value = value_range or [color_min_default, color_max_default]
        camera = relayout_data.get('scene.camera') if relayout_data and 'scene.camera' in relayout_data else None

        show_contours = 'on' in (toggle_contours or [])
        use_black_intervals = 'on' in (toggle_black_intervals or [])
        center_on_zero = 'on' in (center_colormap or [])

        # Si une colormap personnalisée est sélectionnée
        if selected_colormap in saved_colormaps:
            custom_colormap = saved_colormaps[selected_colormap]['data']
        else:
            custom_colormap = selected_colormap

        fig = fct.plot_mesh_with_colorbar(
            vertices, faces, scalars,
            color_min=min_value, color_max=max_value,
            camera=camera,
            show_contours=show_contours,
            colormap=custom_colormap,
            use_black_intervals=use_black_intervals,
            center_colormap_on_zero=center_on_zero
        )
        return fig

    @app.callback(
        Output('colormap-dropdown', 'options'),
        [Input('colormap-type-dropdown', 'value')]
    )
    def update_colormap_options(selected_type):
        if selected_type == 'custom':
            options = [{"label": name, "value": name} for name in saved_colormaps.keys()]
        else:
            options = [{"label": cmap, "value": cmap} for cmap in fct.get_colorscale_names(selected_type)]
        return options
