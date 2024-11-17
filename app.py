import json
import streamlit as st
from streamlit_lottie import st_lottie

# Configure Streamlit page
st.set_page_config(page_title="View Modified Tree Animation", layout="wide")

# Load the JSON file (modified_tree_animation.json) with st.cache_data
@st.cache_data
def load_json():
    """
    Load the modified JSON file for visualization.
    """
    with open("modified_tree_animation.json", "r") as f:
        return json.load(f)

# Main Streamlit app function
def main():
    st.title("View Modified Tree Animation")
    st.markdown("This app visualizes the downloaded modified JSON file as is.")

    # Load JSON data from modified_tree_animation.json
    json_data = load_json()

    # Render the JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(json_data, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
