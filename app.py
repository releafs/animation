import json
import base64
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML

# Initialize the Dash app
app = dash.Dash(__name__)

# Load JSON data from tree.json
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Function to convert JSON to a base64 string for embedding
def json_to_base64(json_data):
    json_str = json.dumps(json_data)
    return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

# Load the initial JSON data
json_data = load_json()

# Generate controls for each tree layer in the JSON data
controls_children = []
tree_indices = []
for index, layer in enumerate(json_data.get("layers", [])):
    if "tree" in layer.get("nm", "").lower():
        tree_indices.append(index)
        position = layer["ks"]["p"]["k"]
        scale = layer["ks"]["s"]["k"]

        # Create sliders for position and scale controls
        controls_children.append(html.Div([
            html.H3(f"Tree {index + 1}"),
            html.Label(f"Position X"),
            dcc.Slider(
                id={'type': 'pos-x', 'index': index},
                min=0,
                max=1600,
                step=10,
                value=int(position[0])
            ),
            html.Label(f"Position Y"),
            dcc.Slider(
                id={'type': 'pos-y', 'index': index},
                min=0,
                max=1200,
                step=10,
                value=int(position[1])
            ),
            html.Label(f"Scale"),
            dcc.Slider(
                id={'type': 'scale', 'index': index},
                min=50,
                max=300,
                step=10,
                value=int(scale[0])
            ),
        ]))

# Get the base64 JSON for initial rendering
initial_base64_json = json_to_base64(json_data)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Interactive Tree Animation Editor"),

    # Controls
    html.Div(controls_children),

    # Button to update the animation
    html.Button('Update Animation', id='update-button', n_clicks=0),

    # Container for the Lottie animation
    html.Div(id='animation-container', children=[
        DangerouslySetInnerHTML(f'''
            <div id="lottie-animation" style="width:100%; height:400px;"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.4/lottie.min.js"></script>
            <script>
                var animationData = JSON.parse(atob("{initial_base64_json}"));
                var params = {{
                    container: document.getElementById('lottie-animation'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    animationData: animationData
                }};
                window.anim = lottie.loadAnimation(params);
            </script>
        ''')
    ])
])

# Define callback to update the animation when sliders change
@app.callback(
    Output('animation-container', 'children'),
    Input('update-button', 'n_clicks'),
    [State({'type': 'pos-x', 'index': ALL}, 'value'),
     State({'type': 'pos-y', 'index': ALL}, 'value'),
     State({'type': 'scale', 'index': ALL}, 'value')]
)
def update_animation(n_clicks, pos_x_values, pos_y_values, scale_values):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate

    # Load the original JSON data again to prevent cumulative modifications
    modified_json = load_json()

    # Modify the JSON data based on the slider values
    for idx, layer in enumerate(modified_json.get("layers", [])):
        if "tree" in layer.get("nm", "").lower():
            # Update position
            layer["ks"]["p"]["k"][0] = pos_x_values[idx]
            layer["ks"]["p"]["k"][1] = pos_y_values[idx]
            # Update scale
            layer["ks"]["s"]["k"][0] = scale_values[idx]
            layer["ks"]["s"]["k"][1] = scale_values[idx]

    # Convert modified JSON to base64
    base64_json = json_to_base64(modified_json)

    # Generate new HTML with updated animation data
    animation_html = DangerouslySetInnerHTML(f'''
        <div id="lottie-animation" style="width:100%; height:400px;"></div>
        <script>
            var animationData = JSON.parse(atob("{base64_json}"));
            if(window.anim) {{
                window.anim.destroy();
            }}
            var params = {{
                container: document.getElementById('lottie-animation'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: animationData
            }};
            window.anim = lottie.loadAnimation(params);
        </script>
    ''')

    return [animation_html]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
