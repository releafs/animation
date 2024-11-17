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

# Filter the JSON to keep only 9 trees and arrange them in a 3x3 grid
def filter_and_arrange_trees(json_data, rows=3, cols=3):
    """
    Filter the JSON data to keep only 9 trees and arrange them in a 3x3 grid.
    """
    grid_spacing = 400  # Adjust the spacing between trees
    filtered_layers = []
    tree_count = 0

    for layer in json_data.get("layers", []):
        if "tree" in layer.get("nm", "").lower():
            tree_count += 1
            if tree_count > rows * cols:  # Stop after selecting 9 trees
                break
            
            # Calculate grid positions
            row = (tree_count - 1) // cols
            col = (tree_count - 1) % cols
            new_x = col * grid_spacing + grid_spacing // 2  # Center in cell
            new_y = row * grid_spacing + grid_spacing // 2

            # Update the position of the tree
            layer["ks"]["p"]["k"] = [new_x, new_y, 0]
            filtered_layers.append(layer)

    # Update the JSON to include only filtered layers
    json_data["layers"] = filtered_layers
    return json_data

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Loop through each "tree" in the JSON "layers"
    for index, layer in enumerate(updated_json.get("layers", [])):
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

    # Filter and arrange the trees into a 3x3 grid
    filtered_json = filter_and_arrange_trees(json_data, rows=3, cols=3)

    # Display editable parameters in sidebar and apply changes
    modified_json = display_json_editor(filtered_json)

    # Render the modified JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(modified_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
