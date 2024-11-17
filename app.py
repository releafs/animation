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

# Count the number of trees in the animation
def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    tree_count = 0
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, count the individual shapes
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Each shape could represent a tree
            else:
                tree_count += 1  # Count the layer as one tree if no shapes found
    return tree_count

# Calculate the spacing between trees
def calculate_tree_spacing(json_data):
    """
    Calculate the spacing between trees based on their positions.
    """
    positions = []

    # Collect positions of all trees
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            position = layer.get("ks", {}).get("p", {}).get("k", [])
            if position:
                positions.append((position[0], position[1]))  # (x, y)

    # Sort positions by X and Y for a grid layout
    positions = sorted(positions, key=lambda pos: (pos[1], pos[0]))  # Sort by Y first, then X

    # Calculate differences between consecutive positions
    x_differences = []
    y_differences = []

    for i in range(1, len(positions)):
        x_diff = positions[i][0] - positions[i - 1][0]
        y_diff = positions[i][1] - positions[i - 1][1]

        if x_diff > 0:  # Same row, different X
            x_differences.append(x_diff)
        if y_diff > 0:  # Different row
            y_differences.append(y_diff)

    # Return the most common spacing as the fixed spacing
    avg_x_spacing = sum(x_differences) / len(x_differences) if x_differences else 0
    avg_y_spacing = sum(y_differences) / len(y_differences) if y_differences else 0

    return avg_x_spacing, avg_y_spacing

# Add or remove trees in the animation
def update_tree_count(json_data, desired_count):
    """
    Add or remove trees in the animation to match the desired count.
    """
    current_count = count_trees(json_data)
    layer_template = None

    # Find a template layer for adding new trees
    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            layer_template = layer.copy()
            break

    if not layer_template:
        st.error("No tree layer template found in the JSON.")
        return json_data

    # Add trees if the count is less than desired
    if desired_count > current_count:
        for _ in range(desired_count - current_count):
            new_layer = layer_template.copy()
            # Change position slightly for the new tree
            new_layer["ks"]["p"]["k"][0] += 50  # Shift X position
            new_layer["ks"]["p"]["k"][1] += 50  # Shift Y position
            json_data["layers"].append(new_layer)

    # Remove trees if the count is more than desired
    elif desired_count < current_count:
        tree_layers = [layer for layer in json_data.get("layers", []) if "tree" in layer.get("nm", "").lower()]
        json_data["layers"] = [layer for layer in json_data["layers"] if layer not in tree_layers[:current_count - desired_count]]

    return json_data

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Count trees and calculate spacing
    tree_count = count_trees(json_data)
    x_spacing, y_spacing = calculate_tree_spacing(json_data)

    # Display tree count and spacing
    st.sidebar.info(f"Number of Trees: {tree_count}")
    st.sidebar.info(f"Tree Spacing (X, Y): ({x_spacing:.2f}, {y_spacing:.2f})")

    # Allow user to modify the number of trees
    desired_count = st.sidebar.slider("Set Number of Trees", min_value=1, max_value=100, value=tree_count)
    if desired_count != tree_count:
        updated_json = update_tree_count(updated_json, desired_count)

    # Loop through each tree layer for additional modifications
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
