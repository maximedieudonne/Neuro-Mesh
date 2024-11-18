from dash.dependencies import Input, Output, State
import fonctions as fct
import numpy as np

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
    color_min_default, color_max_default = (np.min(scalars), np.max(scalars)) if scalars is not None else (0, 1)

    # Callback pour mettre à jour la figure 3D
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
        # Gestion des valeurs par défaut
        min_value, max_value = value_range or [color_min_default, color_max_default]
        camera = relayout_data.get('scene.camera') if relayout_data and 'scene.camera' in relayout_data else None

        # Options booléennes basées sur les sélections utilisateur
        show_contours = 'on' in (toggle_contours or [])
        use_black_intervals = 'on' in (toggle_black_intervals or [])
        center_on_zero = 'on' in (center_colormap or [])

        # Génération de la figure avec les paramètres mis à jour
        fig = fct.plot_mesh_with_colorbar(
            vertices, faces, scalars,
            color_min=min_value, color_max=max_value,
            camera=camera,
            show_contours=show_contours,
            colormap=selected_colormap,
            use_black_intervals=use_black_intervals,
            center_colormap_on_zero=center_on_zero
        )
        return fig

    # Callback pour mettre à jour la liste des colormaps en fonction du type choisi
    @app.callback(
        Output('colormap-dropdown', 'options'),
        [Input('colormap-type-dropdown', 'value')]
    )
    def update_colormap_options(selected_type):
        # Récupérer les noms des colormaps basés sur le type sélectionné
        colormaps = fct.get_colorscale_names(selected_type)
        return [{'label': cmap, 'value': cmap} for cmap in colormaps]
