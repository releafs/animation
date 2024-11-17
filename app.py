import streamlit as st
from streamlit_lottie import st_lottie
from json import load_json, prepare_json  # Import functions from json.py

# Configure Streamlit page
st.set_page_config(page_title="Tree Animation Preview", layout="wide")

def main():
    st.title("Tree Animation Preview")
    st.markdown("This animation uses the default parameters for the tree shapes and 'rows of trees'.")

    # Load JSON data from tree.json
    json_data = load_json()

    # Prepare the JSON by filtering tree shapes and setting default values
    prepared_json = prepare_json(json_data)

    # Render the prepared JSON animation
    st.subheader("Live Animation Preview")
    st_lottie(prepared_json, key="tree_animation")

# Run the Streamlit app
if __name__ == "__main__":
    main()
