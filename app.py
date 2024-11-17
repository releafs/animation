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
def apply_offsets(json_data, num_duplicates, offsets):
    """
    Create duplicates of the animation with specified offsets.
    """
    duplicated_data = copy.deepcopy(json_data)

    # Duplicate the layers for each copy
    for i in range(1, num_duplicates + 1):
        for layer in json_data.get("layers", []):
            # Create a duplicate of the layer
            duplicated_layer = copy.deepcopy(layer)
            duplicated_layer["nm"] = f"{layer['nm']} - Copy {i}"  # Update the name for the duplicate
            
            # Apply offsets to position
            if "ks" in duplicated_layer and "p" in duplicated_layer["ks"]:
                duplicated_layer["ks"]["p"]["k"][0] += offsets["x"] * i  # Offset X
                duplicated_layer["ks"]["p"]["k"][1] += offsets["y"] * i  # Offset Y
            
            # Add the duplicated layer to the layers
            duplicated_data["layers"].append(duplicated_layer)

    return duplicated_data

# Render Lottie with zoom functionality using HTML
def render_lottie_with_zoom(lottie_data, zoom_level, preview_width, preview_height):
    """
    Embed Lottie animation in HTML with adjustable zoom and preview dimensions.
    Ensures the animation is centered correctly.
    """
    html_content = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: {preview_width}px; height: {preview_height}px; overflow: hidden; background-color: white;">
        <div style="transform: scale({zoom_level}); transform-origin: center center; width: 100%; height: 100%;">
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
    st.title("Duplicate and Offset Tree Animation with Zoom and Dimension Controls")
    st.markdown("Use the sidebar to control duplication, offsets, zoom level, and preview dimensions.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls for duplication
    st.sidebar.header("Duplication Settings")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    offset_x = st.sidebar.number_input(
        "Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    offset_y = st.sidebar.number_input(
        "Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10
    )

    # Sidebar control for zoom
    st.sidebar.header("Zoom Settings")
    zoom_level = st.sidebar.slider("Zoom Level", min_value=0.5, max_value=3.0, value=1.0, step=0.1)

    # Sidebar controls for preview dimensions
    st.sidebar.header("Preview Dimensions")
    preview_width = st.sidebar.number_input(
        "Preview Width (pixels)", min_value=400, max_value=2000, value=800, step=50
    )
    preview_height = st.sidebar.number_input(
        "Preview Height (pixels)", min_value=400, max_value=2000, value=600, step=50
    )

    # Prepare offsets dictionary
    offsets = {"x": offset_x, "y": offset_y}

    # Apply duplication and offsets
    modified_json = apply_offsets(json_data, num_duplicates, offsets)

    # Render the modified JSON animation with zoom and dimensions
    st.subheader("Live Animation Preview")
    zoom_html = render_lottie_with_zoom(modified_json, zoom_level, preview_width, preview_height)
    st.components.v1.html(zoom_html, height=preview_height + 100)

# Run the Streamlit app
if __name__ == "__main__":
    main()
