import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Duplicate and Offset Tree Animation with Zoom", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Duplicate and apply offsets
def apply_offsets(json_data, num_duplicates, original_offsets, duplicate_offsets):
    """
    Apply offsets to the original animation and create duplicates with specified offsets.
    """
    modified_data = copy.deepcopy(json_data)

    # Apply offsets to the original animation
    for layer in modified_data.get("layers", []):
        if "ks" in layer and "p" in layer["ks"]:
            layer["ks"]["p"]["k"][0] += original_offsets["x"]  # Offset X for original animation
            layer["ks"]["p"]["k"][1] += original_offsets["y"]  # Offset Y for original animation

    # Duplicate the layers for each copy
    for i in range(1, num_duplicates + 1):
        for layer in json_data.get("layers", []):
            # Create a duplicate of the layer
            duplicated_layer = copy.deepcopy(layer)
            duplicated_layer["nm"] = f"{layer['nm']} - Copy {i}"  # Update the name for the duplicate

            # Apply offsets to position
            if "ks" in duplicated_layer and "p" in duplicated_layer["ks"]:
                duplicated_layer["ks"]["p"]["k"][0] += duplicate_offsets["x"] * i  # Offset X for duplicates
                duplicated_layer["ks"]["p"]["k"][1] += duplicate_offsets["y"] * i  # Offset Y for duplicates

            # Add the duplicated layer to the layers
            modified_data["layers"].append(duplicated_layer)

    return modified_data

# Render Lottie with zoom functionality and adjustable display size using HTML
def render_lottie_with_zoom(lottie_data, zoom_level, display_height):
    """
    Embed Lottie animation in HTML with adjustable zoom using CSS transforms and adjustable display size.
    """
    html_content = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: {display_height}px; overflow: hidden;">
        <div style="transform: scale({zoom_level}); transform-origin: center;">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.6/lottie.min.js"></script>
            <div id="lottie-animation"></div>
            <script>
                var animationData = {json.dumps(lottie_data)};
                var anim = lottie.loadAnimation({{
                    container: document.getElementById('lottie-animation'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    animationData: animationData
                }});
            </script>
        </div>
    </div>
    """
    return html_content

# Main Streamlit app function
def main():
    st.title("Duplicate and Offset Tree Animation with Adjustable Display")
    st.markdown("Use the sidebar to control offsets for the original animation and duplicates, zoom, and adjust the display size.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls for original offsets
    st.sidebar.header("Original Animation Offsets")
    original_offset_x = st.sidebar.number_input(
        "Original Offset X (pixels)", min_value=-2000, max_value=2000, value=0, step=50
    )
    original_offset_y = st.sidebar.number_input(
        "Original Offset Y (pixels)", min_value=-2000, max_value=2000, value=0, step=50
    )

    # Sidebar controls for duplication
    st.sidebar.header("Duplication Settings")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    duplicate_offset_x = st.sidebar.number_input(
        "Duplicate Offset X (pixels)", min_value=-1000, max_value=1000, value=100, step=50
    )
    duplicate_offset_y = st.sidebar.number_input(
        "Duplicate Offset Y (pixels)", min_value=-1000, max_value=1000, value=100, step=50
    )

    # Sidebar control for zoom
    st.sidebar.header("Zoom Settings")
    zoom_level = st.sidebar.slider("Zoom Level", min_value=0.5, max_value=3.0, value=1.0, step=0.1)

    # Sidebar control for display height
    st.sidebar.header("Display Settings")
    display_height = st.sidebar.number_input(
        "Display Height (pixels)", min_value=400, max_value=2000, value=600, step=50
    )

    # Prepare offsets dictionaries
    original_offsets = {"x": original_offset_x, "y": original_offset_y}
    duplicate_offsets = {"x": duplicate_offset_x, "y": duplicate_offset_y}

    # Apply offsets to original animation and duplicates
    modified_json = apply_offsets(json_data, num_duplicates, original_offsets, duplicate_offsets)

    # Render the modified JSON animation with zoom and adjustable display size
    st.subheader("Live Animation Preview")
    zoom_html = render_lottie_with_zoom(modified_json, zoom_level, display_height)
    st.components.v1.html(zoom_html, height=display_height + 100)

# Run the Streamlit app
if __name__ == "__main__":
    main()
