import streamlit as st
from components.upload import render_upload_section
from components.analysis import render_analysis_section
from components.search import render_search_section

def main():
    st.set_page_config(page_title="Data Buster", page_icon="🧪", layout="wide")

    # Initialize session state variables
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'smiles_column' not in st.session_state:
        st.session_state.smiles_column = None
    if 'activity_column' not in st.session_state:
        st.session_state.activity_column = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    st.title("Data Buster 🧪")

    # Sidebar with upload section
    with st.sidebar:
        render_upload_section()

    # Main content area
    if st.session_state.uploaded_data is None:
        st.info("Please upload a dataset using the sidebar to begin analysis.")
        return

    # Create tabs for different sections
    tabs = st.tabs(["Analysis", "Search"])

    with tabs[0]:
        render_analysis_section()

    with tabs[1]:
        render_search_section()

if __name__ == "__main__":
    main()