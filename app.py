import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees and show layer breakdown
def count_trees_with_layer_info(json_data):
    """
    Count the number of trees in the animation JSON and identify which layer they belong to.
    Returns:
        - Total tree count
        - Layer-wise breakdown
    """
    total_trees = 0
    layer_tree_counts = {}  # To store tree count per layer

    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count = len(layer["shapes"])  # Count shapes in the layer
                layer_tree_counts[layer["nm"]] = tree_count
                total_trees += tree_count
            else:
                layer_tree_counts[layer["nm"]] = 1  # Count the layer as one tree if no shapes found
                total_trees += 1

    return total_trees, layer_tree_counts

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the total tree count and layer-wise breakdown
    total_trees, layer_tree_counts = count_trees_with_layer_info(json_data)
    st.sidebar.info(f"Number of Trees: {total_trees}")

    # Show layer-wise breakdown
    st.sidebar.subheader("Tree Count per Layer")
    for layer_name, count in layer_tree_counts.items():
        st.sidebar.write(f"{layer_name}: {count} trees")

    # Loop through each "tree" in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", ""):  # Check if layer is a tree layer
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

            # Update the layer in the JSON data
            updated_json["layers"][index] = layer

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

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
