import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")


@st.cache(allow_output_mutation=True)
def load_json():
    """
    Load the JSON file (tree.json).
    """
    with open("tree.json", "r") as f:
        return json.load(f)


def calculate_grid_positions(rows, cols, x_start=400, y_start=400, x_gap=400, y_gap=400):
    """
    Calculate grid positions for a given number of rows and columns.
    """
    positions = []
    for row in range(rows):
        for col in range(cols):
            x = x_start + col * x_gap
            y = y_start + row * y_gap
            positions.append([x, y, 0])  # Append 3D position (x, y, z)
    return positions


def arrange_trees_in_grid(json_data, grid_rows=3, grid_cols=3):
    """
    Filter and arrange tree layers into a grid layout.
    """
    updated_json = json_data.copy()

    # Identify tree layers
    tree_layers = [
        layer for layer in updated_json.get("layers", [])
        if "tree" in layer.get("nm", "").lower()
    ]

    # Calculate grid positions for the specified rows and columns
    grid_positions = calculate_grid_positions(grid_rows, grid_cols)

    # Select the required number of trees (grid_rows * grid_cols)
    num_required_trees = grid_rows * grid_cols
    selected_trees = tree_layers[:num_required_trees]

    # Update positions of selected trees
    for idx, tree in enumerate(selected_trees):
        tree["ks"]["p"]["k"] = grid_positions[idx]

    # Replace the original layers with updated tree layers and keep other layers
    updated_json["layers"] = selected_trees + [
        layer for layer in updated_json.get("layers", [])
        if "tree" not in layer.get("nm", "").lower()
    ]

    return updated_json


def count_trees(json_data):
    """
    Count the number of tree objects in the animation JSON.
    """
    return sum(1 for layer in json_data.get("layers", []) if "tree" in layer.get("nm", "").lower())


def main():
    st.title("Interactive Tree Animation Editor")
    st.markdown("Use the sidebar to adjust the tree animation parameters.")

    # Load JSON data
    json_data = load_json()

    # Sidebar options
    st.sidebar.header("Settings")
    rows = st.sidebar.slider("Number of Rows", 1, 5, 3)
    cols = st.sidebar.slider("Number of Columns", 1, 5, 3)

    # Update JSON to arrange trees in a grid
    modified_json = arrange_trees_in_grid(json_data, grid_rows=rows, grid_cols=cols)

    # Display number of trees
    st.sidebar.info(f"Number of Trees: {rows * cols}")

    # Render the modified animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")


if __name__ == "__main__":
    main()
