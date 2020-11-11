import dash

external_scripts = ["https://rawgit.com/neo4j-contrib/neovis.js/master/dist/neovis.js"]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    title='MultiCategory',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True