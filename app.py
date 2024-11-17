import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Editor", layout="wide")

# Allowed shape indices
ALLOWED_SHAPES = [7, 9, 10, 11, 14, 15, 17, 19, 20, 21, 22, 25]

# Default position and scale for "rows of trees"
DEFAULT_POSITION_X = 1160
DEFAULT_POSITION_Y = 710
DEFAULT_SCALE = 400

# Load the JSON file (tree.json) with st.cache_data
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Filter tree shapes in the JSON based on ALLOWED_SHAPES and set default values
def prepare_json(json_data):
    """
    Filters the tree shapes to include only those with indices in ALLOWED_SHAPES
    and applies default position and scale for the "rows of trees" layer.
    """
    filtered_data = json_data.copy()
    
    for layer in filtered_data.get("layers", []):
        # Check if the layer is named "tree" or contains tree objects
        if "tree" in layer.get("nm", "").lower():
            # If the layer has shapes, filter only allowed shapes
            if "shapes" in layer:
                layer["shapes"] = [
                    shape for i, shape in enumerate(layer["shapes"]) if (i + 1) in ALLOWED_SHAPES
                ]
            # Apply default position and scale for "rows of trees"
            if "rows of trees" in layer.get("nm", "").lower():
                layer["ks"]["p"]["k"] = [DEFAULT_POSITION_X, DEFAULT_POSITION_Y, 0]  # Position
                layer["ks"]["s"]["k"] = [DEFAULT_SCALE, DEFAULT_SCALE, 100]  # Scale
    return filtered_data

# Main Streamlit app function
def main():
    st.title("Tree Animation Preview and Download")
    st.markdown("This animation uses the default parameters for the tree shapes and 'rows of trees'.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Prepare the JSON by filtering tree shapes and setting default values
    prepared_json = prepare_json(json_data)

    # Render the prepared JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(prepared_json, key="tree_animation")

    # Provide a download button for the modified JSON
    st.subheader("Download Modified JSON")
    json_str = json.dumps(prepared_json, indent=4)  # Convert JSON to a string with pretty formatting
    st.download_button(
        label="Download JSON File",
        data=json_str,
        file_name="modified_tree_animation.json",
        mime="application/json"
    )

# Run the Streamlit app
if __name__ == "__main__":
    main()
