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
            if "shapes" in layer:
                tree_count += len(layer["shapes"])  # Count shapes as trees
            else:
                tree_count += 1  # Count as one tree if no shapes
    return tree_count

# Add or remove trees dynamically
def adjust_tree_count(json_data, desired_count, spacing=200):
    """
    Adjust the number of tree layers to match the desired count.
    New trees will follow a consistent spacing rule.
    """
    current_count = count_trees(json_data)
    updated_json = json_data.copy()

    if current_count < desired_count:
        # Add more trees
        for i in range(desired_count - current_count):
            # Clone the first tree layer as a template
            template_layer = next(
                (layer for layer in updated_json["layers"] if "tree" in layer.get("nm", "").lower()), None
            )
            if template_layer:
                new_layer = template_layer.copy()
                new_layer["nm"] = f"tree_{current_count + i + 1}"  # Update tree name
                # Adjust position (place next to the existing trees)
                new_x_position = template_layer["ks"]["p"]["k"][0] + (i + 1) * spacing
                new_layer["ks"]["p"]["k"][0] = new_x_position
                updated_json["layers"].append(new_layer)
    elif current_count > desired_count:
        # Remove extra trees
        updated_json["layers"] = [
            layer for layer in updated_json["layers"] if not ("tree" in layer.get("nm", "").lower() and int(layer.get("nm", "").split("_")[-1]) > desired_count)
        ]

    return updated_json

# Display parameters and allow editing in Streamlit sidebar
def display_json_editor(json_data):
    updated_json = json_data.copy()  # Create a copy to store modifications
    st.sidebar.header("Edit Tree Animation Parameters")

    # Get current tree count
    current_count = count_trees(json_data)

    # Slider to adjust the number of trees
    desired_count = st.sidebar.slider("Number of Trees", min_value=1, max_value=100, value=current_count, step=1)

    # Adjust the tree count dynamically
    updated_json = adjust_tree_count(updated_json, desired_count)

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
