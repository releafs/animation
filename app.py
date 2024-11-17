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

def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    tree_count = 0
    for layer in json_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Each shape could represent a tree
            else:
                tree_count += 1  # Count the layer as one tree if no shapes found
    return tree_count

def get_unique_tree_types(json_data):
    """
    Identify unique tree types based on shape and color properties.
    """
    unique_trees = set()
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            if "shapes" in layer:
                for shape in layer["shapes"]:
                    # Extract the key properties for identifying unique shapes
                    shape_data = {
                        "path": shape.get("ks", {}).get("k", {}),  # Shape path
                        "fill": shape.get("c", {}).get("k", {})  # Fill color
                    }
                    unique_trees.add(json.dumps(shape_data, sort_keys=True))  # Serialize for uniqueness
    return len(unique_trees), [json.loads(tree) for tree in unique_trees]  # Deserialize for debugging

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees and unique types
    tree_count = count_trees(json_data)
    unique_tree_count, unique_trees = get_unique_tree_types(json_data)

    # Display counts in the sidebar
    st.sidebar.info(f"Number of Trees: {tree_count}")
    st.sidebar.info(f"Number of Unique Tree Types: {unique_tree_count}")

    # Optionally display details of unique tree types
    if st.sidebar.checkbox("Show Unique Tree Types"):
        st.sidebar.text("Unique Trees (Debug):")
        st.sidebar.json(unique_trees)

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
