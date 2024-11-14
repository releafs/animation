import json
import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS, Slider
from bokeh.layouts import column
import base64

# Load JSON from tree.json
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Display JSON parameters for editing
def display_json_editor(json_data):
    updated_json = json_data.copy()
    st.sidebar.header("Edit Tree Animation Parameters")

    # Loop through each tree layer in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", ""):
            st.sidebar.subheader(f"Tree {index + 1}")

            # Edit position (x, y)
            position = layer["ks"]["p"]["k"]
            new_x = st.sidebar.slider(f"Tree {index + 1} Position X", 0, 1600, int(position[0]), step=10)
            new_y = st.sidebar.slider(f"Tree {index + 1} Position Y", 0, 1200, int(position[1]), step=10)
            layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"Tree {index + 1} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

            updated_json["layers"][index] = layer

    return updated_json

# Render Lottie animation as iframe with real-time updates
def render_lottie_iframe(json_data):
    json_str = json.dumps(json_data)
    json_base64 = base64.b64encode(json_str.encode()).decode()
    html_code = f"""
    <iframe src="https://lottiefiles.com/preview/{json_base64}" 
            style="width:100%; height:400px; border:none;"></iframe>
    """
    st.components.v1.html(html_code, height=450)

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")

    # Load JSON data from tree.json
    json_data = load_json()

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data)

    # Display JSON structure for reference
    st.subheader("Modified JSON Structure")
    st.json(modified_json)

    # Render the Lottie animation as an iframe
    st.subheader("Live Animation Preview")
    render_lottie_iframe(modified_json)

# Run the Streamlit app
if __name__ == "__main__":
    main()
