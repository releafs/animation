import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Scale Factor for Tree Animation", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Apply offsets to the original animation
def apply_original_offsets(json_data, offsets):
    """
    Apply offsets to the original animation layers.
    """
    modified_data = copy.deepcopy(json_data)
    for layer in modified_data.get("layers", []):
        if "ks" in layer and "p" in layer["ks"]:
            layer["ks"]["p"]["k"][0] += offsets["x"]  # Offset X
            layer["ks"]["p"]["k"][1] += offsets["y"]  # Offset Y
    return modified_data

# Duplicate and apply offsets
def apply_duplicates(json_data, num_duplicates, offsets):
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

# Render Lottie with scale factor using CSS
def render_lottie_with_scale(lottie_data, original_scale, duplicate_scale):
    """
    Embed Lottie animation in HTML with adjustable scale factors for original and duplicates.
    """
    html_content = f"""
    <div style="display: flex; flex-direction: column; align-items: center; gap: 20px; overflow: hidden;">
        <!-- Original Animation -->
        <div style="transform: scale({original_scale}); transform-origin: center; border: 1px solid gray; padding: 10px;">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.6/lottie.min.js"></script>
            <div id="original-animation"></div>
            <script>
                var originalData = {json.dumps(lottie_data)};
                lottie.loadAnimation({{
                    container: document.getElementById('original-animation'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    animationData: originalData
                }});
            </script>
        </div>

        <!-- Duplicates -->
        <div style="transform: scale({duplicate_scale}); transform-origin: center; border: 1px solid gray; padding: 10px;">
            <div id="duplicate-animation"></div>
            <script>
                var duplicateData = {json.dumps(lottie_data)};
                lottie.loadAnimation({{
                    container: document.getElementById('duplicate-animation'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    animationData: duplicateData
                }});
            </script>
        </div>
    </div>
    """
    return html_content

# Main Streamlit app function
def main():
    st.title("Tree Animation with Independent Scale Factor")
    st.markdown(
        "Use the sidebar to control offsets, number of duplicates, and scale factors for the original and duplicate animations."
    )

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Sidebar controls for the original animation offsets
    st.sidebar.header("Original Animation Offset and Scale")
    original_offset_x = st.sidebar.number_input(
        "Original Offset X (pixels)", min_value=-500, max_value=500, value=0, step=10
    )
    original_offset_y = st.sidebar.number_input(
        "Original Offset Y (pixels)", min_value=-500, max_value=500, value=0, step=10
    )
    original_scale = st.sidebar.slider(
        "Original Animation Scale", min_value=0.5, max_value=3.0, value=1.0, step=0.1
    )

    # Sidebar controls for duplication
    st.sidebar.header("Duplication Settings and Scale")
    num_duplicates = st.sidebar.number_input(
        "Number of Duplicates", min_value=0, max_value=10, value=2, step=1
    )
    duplicate_offset_x = st.sidebar.number_input(
        "Duplicate Offset X (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    duplicate_offset_y = st.sidebar.number_input(
        "Duplicate Offset Y (pixels)", min_value=-500, max_value=500, value=100, step=10
    )
    duplicate_scale = st.sidebar.slider(
        "Duplicate Animation Scale", min_value=0.5, max_value=3.0, value=1.0, step=0.1
    )

    # Prepare offsets dictionaries
    original_offsets = {"x": original_offset_x, "y": original_offset_y}
    duplicate_offsets = {"x": duplicate_offset_x, "y": duplicate_offset_y}

    # Apply original offsets
    modified_json = apply_original_offsets(json_data, original_offsets)

    # Apply duplication and offsets
    modified_json = apply_duplicates(modified_json, num_duplicates, duplicate_offsets)

    # Render the modified JSON animation with independent scale factors
    st.subheader("Live Animation Preview")
    scale_html = render_lottie_with_scale(modified_json, original_scale, duplicate_scale)
    st.components.v1.html(scale_html, height=800)

# Run the Streamlit app
if __name__ == "__main__":
    main()
