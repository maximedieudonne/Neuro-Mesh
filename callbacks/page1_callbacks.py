from dash.dependencies import Input, Output, State
import dash_uploader as du
import fonctions as fct
import numpy as np
import os
from dash import callback_context

# Default paths
DEFAULT_MESH_PATH = './data/mesh.gii'
DEFAULT_TEXTURE_PATH = './data/texture.gii'

# Temporary upload directory
UPLOAD_DIRECTORY = "./uploaded_files/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def register_callbacks(app):
    # Variables to store the current mesh and texture
    global current_mesh, current_vertices, current_faces, current_scalars
    current_mesh = fct.load_mesh(DEFAULT_MESH_PATH)
    current_vertices = current_mesh.vertices
    current_faces = current_mesh.faces
    current_scalars = fct.read_gii_file(DEFAULT_TEXTURE_PATH) if DEFAULT_TEXTURE_PATH else None

    color_min_default, color_max_default = (
        (np.min(current_scalars), np.max(current_scalars)) if current_scalars is not None else (0, 100)
    )

    # Configure Dash Uploader to allow drag-and-drop
    du.configure_upload(
        app,
        UPLOAD_DIRECTORY,
        use_upload_id=False,  # Simplify directory management
    )

    @app.callback(
        Output('3d-mesh', 'figure'),
        [
            Input('range-slider', 'value'),
            Input('toggle-contours', 'value'),
            Input('toggle-black-intervals', 'value'),
            Input('colormap-dropdown', 'value'),
            Input('toggle-center-colormap', 'value'),
            Input('upload-mesh', 'isCompleted'),
            Input('upload-texture', 'isCompleted'),
        ],
        [
            State('3d-mesh', 'relayoutData'),
            State('upload-mesh', 'fileNames'),
            State('upload-texture', 'fileNames'),
        ],
    )
    def update_figure(
        value_range,
        toggle_contours,
        toggle_black_intervals,
        selected_colormap,
        center_colormap,
        mesh_uploaded,
        texture_uploaded,
        relayout_data,
        mesh_files,
        texture_files,
    ):
        global current_mesh, current_vertices, current_faces, current_scalars
        triggered = callback_context.triggered

        # Handle new mesh upload
        if any("upload-mesh" in t["prop_id"] for t in triggered):
            if mesh_uploaded and mesh_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, mesh_files[0])
                current_mesh = fct.load_mesh(uploaded_file)
                current_vertices = current_mesh.vertices
                current_faces = current_mesh.faces
                current_scalars = None  # Reset texture

        # Handle new texture upload
        elif any("upload-texture" in t["prop_id"] for t in triggered):
            if texture_uploaded and texture_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, texture_files[0])
                current_scalars = fct.read_gii_file(uploaded_file)

        # Handle regular updates (sliders, dropdowns, etc.)
        min_value, max_value = value_range or [color_min_default, color_max_default]
        camera = relayout_data.get('scene.camera') if relayout_data and 'scene.camera' in relayout_data else None

        show_contours = 'on' in (toggle_contours or [])
        use_black_intervals = 'on' in (toggle_black_intervals or [])
        center_on_zero = 'on' in (center_colormap or [])

        fig = fct.plot_mesh_with_colorbar(
            current_vertices,
            current_faces,
            current_scalars,
            color_min=min_value,
            color_max=max_value,
            camera=camera,
            show_contours=show_contours,
            colormap=selected_colormap,
            use_black_intervals=use_black_intervals,
            center_colormap_on_zero=center_on_zero,
        )
        return fig

    @app.callback(
        Output('colormap-dropdown', 'options'),
        [Input('colormap-type-dropdown', 'value')],
    )
    def update_colormap_options(selected_type):
        return [{"label": cmap, "value": cmap} for cmap in fct.get_colorscale_names(selected_type)]
