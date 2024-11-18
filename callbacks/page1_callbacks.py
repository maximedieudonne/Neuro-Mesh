from dash.dependencies import Input, Output

def register_callbacks(app):
    @app.callback(
        Output('color-output', 'children'),
        Input('color-picker', 'value'),
    )
    def update_color_output(selected_color):
        if selected_color:
            return f"You selected: {selected_color}"
        return "Please select a color."
