from dash import Dash

# Initialise une instance unique de l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Improved Dashboard"
