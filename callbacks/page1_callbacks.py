from dash.dependencies import Input, Output, State
import dash_uploader as du
import fonctions as fct
import numpy as np
import os
from dash import callback_context

UPLOAD_DIRECTORY = "./uploaded_files/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def register_callbacks(app):
    global current_mesh, current_vertices, current_faces, current_scalars
    current_mesh = fct.load_mesh('./data/mesh.gii')
    current_vertices, current_faces = current_mesh.vertices, current_mesh.faces
    current_scalars = fct.read_gii_file('./data/texture.gii')

    du.configure_upload(app, UPLOAD_DIRECTORY, use_upload_id=False)

    @app.callback(
        [
            Output('3d-mesh', 'figure'),
            Output('upload-status', 'children'),
        ],
        [
            Input('upload-mesh', 'isCompleted'),
            Input('upload-texture', 'isCompleted'),
            Input('range-slider', 'value'),
            Input('toggle-contours', 'value'),
            Input('toggle-black-intervals', 'value'),
            Input('colormap-dropdown', 'value'),
            Input('toggle-center-colormap', 'value'),
        ],
        [
            State('upload-mesh', 'fileNames'),
            State('upload-texture', 'fileNames'),
        ],
    )
    def update_figure(
        mesh_uploaded, texture_uploaded, value_range, toggle_contours,
        toggle_black_intervals, selected_colormap, center_colormap, mesh_files, texture_files
    ):
        global current_mesh, current_vertices, current_faces, current_scalars

        triggered = callback_context.triggered
        feedback = None

        # Handle new mesh upload
        if any("upload-mesh" in t["prop_id"] for t in triggered):
            if mesh_uploaded and mesh_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, mesh_files[0])
                current_mesh = fct.load_mesh(uploaded_file)
                current_vertices, current_faces = current_mesh.vertices, current_mesh.faces
                current_scalars = None  # Reset texture
                feedback = f"Maillage {mesh_files[0]} chargé avec succès."
                return (
                    fct.plot_mesh_with_colorbar(current_vertices, current_faces, None),
                    feedback
                )

        # Handle new texture upload
        if any("upload-texture" in t["prop_id"] for t in triggered):
            if texture_uploaded and texture_files:
                uploaded_file = os.path.join(UPLOAD_DIRECTORY, texture_files[0])
                current_scalars = fct.read_gii_file(uploaded_file)
                feedback = f"Texture {texture_files[0]} chargée avec succès."

        # Generate figure with current data
        fig = fct.plot_mesh_with_colorbar(
            current_vertices,
            current_faces,
            current_scalars,
            color_min=value_range[0],
            color_max=value_range[1],
            colormap=selected_colormap,
            show_contours='on' in toggle_contours,
            center_colormap_on_zero='on' in center_colormap,
            use_black_intervals='on' in toggle_black_intervals,
        )
        return fig, feedback
