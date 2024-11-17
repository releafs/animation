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
DEFAULT_GAP = 1500  # Default gap between the two animations

# Load the JSON file (tree.json) with st.cache_data
@st.cache_data
def load_json():
    with open("tree.json", "r") as f:
        return json.load(f)

# Filter tree shapes in the JSON based on ALLOWED_SHAPES and set default values
def prepare_json(json_data, position_x, position_y, scale):
    """
    Filters the tree shapes to include only those with indices in ALLOWED_SHAPES
    and applies position and scale values.
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
            # Apply position and scale values for "rows of trees"
            if "rows of trees" in layer.get("nm", "").lower():
                layer["ks"]["p"]["k"] = [position_x, position_y, 0]  # Position
                layer["ks"]["s"]["k"] = [scale, scale, 100]  # Scale
    return filtered_data

# Main Streamlit app function
def main():
    st.title("Duplicated Tree Animation")
    st.markdown("Control the parameters of the animations in the sidebar.")

    # Sidebar controls
    st.sidebar.header("Animation Controls")
    gap = st.sidebar.slider("Gap Between Animations", 1000, 2000, DEFAULT_GAP, step=50, value=DEFAULT_GAP)
    scale = st.sidebar.slider("Rows of Trees Scale", 100, 1000, DEFAULT_SCALE, step=50, value=DEFAULT_SCALE)
    position_y = st.sidebar.slider("Rows of Trees Position Y", 500, 1000, DEFAULT_POSITION_Y, step=10, value=DEFAULT_POSITION_Y)

    # Load JSON data from tree.json
    json_data = load_json()

    # Prepare the first animation (original position)
    first_animation = prepare_json(json_data, DEFAULT_POSITION_X, position_y, scale)

    # Prepare the second animation (offset by gap)
    second_animation = prepare_json(json_data, DEFAULT_POSITION_X + gap, position_y, scale)

    # Render the animations side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Animation 1")
        st_lottie(first_animation, key="animation1")

    with col2:
        st.subheader("Animation 2")
        st_lottie(second_animation, key="animation2")

# Run the Streamlit app
if __name__ == "__main__":
    main()
