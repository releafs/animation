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

# Count the number of trees and prepare control toggles
def count_trees_with_layer_info(json_data):
    """
    Count the number of trees in the animation JSON and prepare control toggles.
    Returns:
        - Total tree count
        - Layer-wise breakdown with control toggles
    """
    total_trees = 0
    layer_tree_controls = {}  # To store control toggles for trees in each layer

    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count = len(layer["shapes"])  # Count shapes in the layer
                layer_tree_controls[layer["nm"]] = [
                    {"name": f"Tree {i + 1}", "visible": True}
                    for i in range(tree_count)
                ]  # Default all trees to visible
                total_trees += tree_count
            else:
                layer_tree_controls[layer["nm"]] = [
                    {"name": f"Tree 1", "visible": True}
                ]  # Single tree layer
                total_trees += 1

    return total_trees, layer_tree_controls

# Display parameters, toggles, and update JSON in Streamlit sidebar
def display_json_editor(json_data, layer_tree_controls):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the total tree count and layer-wise controls
    total_trees = sum(len(trees) for trees in layer_tree_controls.values())
    st.sidebar.info(f"Number of Trees: {total_trees}")

    # Create control toggles for each layer
    for layer_name, tree_controls in layer_tree_controls.items():
        st.sidebar.subheader(layer_name)
        for i, tree in enumerate(tree_controls):
            tree["visible"] = st.sidebar.checkbox(
                tree["name"], value=tree["visible"]
            )  # Create a toggle for each tree

    # Update JSON based on visibility toggles
    for layer in updated_json.get("layers", []):
        if layer.get("nm", "") in layer_tree_controls:
            # Check shapes and remove invisible trees
            controls = layer_tree_controls[layer["nm"]]
            if "shapes" in layer:
                layer["shapes"] = [
                    shape
                    for i, shape in enumerate(layer["shapes"])
                    if controls[i]["visible"]
                ]

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to toggle tree visibility and adjust animation parameters.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Count trees and generate initial control toggles
    total_trees, layer_tree_controls = count_trees_with_layer_info(json_data)

    # Display controls and apply changes to the JSON
    modified_json = display_json_editor(json_data, layer_tree_controls)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
