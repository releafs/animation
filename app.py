import json
import streamlit as st
from streamlit_lottie import st_lottie
import copy

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Load the JSON file (tree.json)
@st.cache(allow_output_mutation=True)
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Count the number of trees in the animation
def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    return sum(1 for layer in json_data.get("layers", []) if "tree" in layer.get("nm", "").lower())

# Add a new tree layer
def add_tree(json_data):
    """
    Add a new tree layer to the JSON.
    """
    if not json_data.get("layers"):
        return json_data  # Return if there are no layers
    # Use a copy of the last tree layer as a template
    last_tree = next((layer for layer in reversed(json_data["layers"]) if "tree" in layer.get("nm", "").lower()), None)
    if last_tree:
        new_tree = copy.deepcopy(last_tree)
        new_tree["nm"] = f"tree_{len(json_data['layers']) + 1}"  # Rename layer
        new_tree["ks"]["p"]["k"] = [100 * len(json_data["layers"]), 500, 0]  # Adjust position
        json_data["layers"].append(new_tree)
    return json_data

# Remove the last tree layer
def remove_tree(json_data):
    """
    Remove the last tree layer from the JSON.
    """
    json_data["layers"] = [layer for layer in json_data["layers"] if "tree" not in layer.get("nm", "").lower() or len(json_data["layers"]) == 1]
    return json_data

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get the number of trees
    tree_count = count_trees(json_data)

    # Editable number of trees
    st.sidebar.subheader("Manage Trees")
    number_of_trees = st.sidebar.number_input(
        "Number of Trees", min_value=1, max_value=100, value=tree_count, step=1
    )

    # Adjust the number of trees dynamically
    if number_of_trees > tree_count:
        for _ in range(number_of_trees - tree_count):
            updated_json = add_tree(updated_json)
    elif number_of_trees < tree_count:
        for _ in range(tree_count - number_of_trees):
            updated_json = remove_tree(updated_json)

    # Display editable tree parameters
    for index, layer in enumerate(updated_json.get("layers", [])):
        if "tree" in layer.get("nm", "").lower():
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

    return updated_json

# Main Streamlit app function
def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters or change the number of trees.")

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
