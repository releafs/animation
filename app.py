import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Allowed shape indices
ALLOWED_SHAPES = [7, 9, 10, 11, 14, 15, 17, 19, 20, 21, 22, 25]

# Load the JSON file (tree.json) with st.cache_data
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees and collect their labels
def count_trees_with_labels(json_data):
    """
    Count the number of allowed tree shapes in the animation JSON and collect their labels.
    Filters shapes based on ALLOWED_SHAPES.
    """
    tree_count = 0
    tree_labels = []
    
    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, filter only allowed shapes
            if "shapes" in layer:
                for i, shape in enumerate(layer["shapes"]):
                    if (i + 1) in ALLOWED_SHAPES:  # Filter shapes by allowed indices (1-based)
                        tree_count += 1
                        tree_labels.append((f"{layer['nm']} - Shape {i+1}", shape))
            else:
                tree_count += 1
                tree_labels.append((layer["nm"], layer))

    return tree_count, tree_labels

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees and their labels
    tree_count, tree_labels = count_trees_with_labels(json_data)
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Create a dictionary to track visibility of each shape
    visibility = {}

    # Display tree labels with checkboxes
    st.sidebar.subheader("Tree Labels")
    for label, shape in tree_labels:
        # Add a checkbox to toggle visibility
        visibility[label] = st.sidebar.checkbox(label, value=True)

        # Adjust opacity based on visibility
        if isinstance(shape, dict) and "it" in shape:  # Check if shape has sub-items
            for item in shape["it"]:
                if "o" in item:  # Look for opacity property
                    item["o"]["k"] = 100 if visibility[label] else 0
        elif "o" in shape:  # Directly adjust layer opacity
            shape["o"]["k"] = 100 if visibility[label] else 0

    # Allow other parameter adjustments if needed
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", ""):  # Check if layer is a tree layer
            st.sidebar.subheader(f"Edit {layer['nm']}")

            # Edit position (x, y)
            position = layer["ks"]["p"]["k"]
            new_x = st.sidebar.slider(f"{layer['nm']} Position X", 0, 1600, int(position[0]), step=10)
            new_y = st.sidebar.slider(f"{layer['nm']} Position Y", 0, 1200, int(position[1]), step=10)
            layer["ks"]["p"]["k"] = [new_x, new_y, position[2]]

            # Edit scale
            scale = layer["ks"]["s"]["k"]
            new_scale = st.sidebar.slider(f"{layer['nm']} Scale", 50, 300, int(scale[0]), step=10)
            layer["ks"]["s"]["k"] = [new_scale, new_scale, 100]

            # Update the layer in the JSON data
            updated_json["layers"][index] = layer

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters and toggle individual tree shapes.")

    # Load JSON data from tree.json
    json_data = load_json()
    
    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
