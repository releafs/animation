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

# Count the number of trees and collect their labels
def count_trees_with_labels(json_data):
    """
    Count the number of tree objects in the animation JSON and collect their labels.
    Returns a count and a list of labels.
    """
    tree_count = 0
    tree_labels = []
    
    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes and use layer name as a prefix
            if "shapes" in layer:
                shape_count = len(layer["shapes"])
                tree_count += shape_count
                for i in range(shape_count):
                    tree_labels.append(f"{layer['nm']} - Shape {i+1}")
            else:
                tree_count += 1
                tree_labels.append(layer["nm"])

    return tree_count, tree_labels

# Toggle shapes on/off
def toggle_shapes(json_data, toggles):
    """
    Modify the JSON data to toggle visibility of shapes based on user input.
    """
    updated_json = json_data.copy()
    shape_index = 0  # Track the shape index globally

    for layer in updated_json.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes
            if "shapes" in layer:
                for shape in layer["shapes"]:
                    # Use the global shape index to determine toggle status
                    shape["hd"] = not toggles[shape_index]  # Set 'hd' (hidden) property
                    shape_index += 1
            else:
                # For layers without shapes, toggle visibility using 'hd'
                layer["hd"] = not toggles[shape_index]
                shape_index += 1

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to toggle tree shapes and edit parameters. Apply changes to refresh the animation.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Get the number of trees and their labels
    tree_count, tree_labels = count_trees_with_labels(json_data)

    # Sidebar - Toggles for each tree shape
    st.sidebar.header("Tree Labels and Toggles")
    st.sidebar.info(f"Number of Trees: {tree_count}")

    # Create toggles for each tree
    toggles = []
    for label in tree_labels:
        toggles.append(st.sidebar.checkbox(f"Show {label}", value=True))

    # Sidebar - Apply Button
    if st.sidebar.button("Apply Changes"):
        # Update JSON based on toggles and refresh animation
        modified_json = toggle_shapes(json_data, toggles)
        st.session_state["modified_json"] = modified_json  # Store the modified JSON in session state
    else:
        # Load from session state if available
        modified_json = st.session_state.get("modified_json", json_data)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
