import streamlit as st
from utils.data_processing import DataProcessor
import pandas as pd

def render_column_selector(df: pd.DataFrame, column_type: str, key_prefix: str):
    """Render an improved column selector with preview"""
    columns = df.columns.tolist()
    
    selected_column = st.selectbox(
        f"Select {column_type} column",
        options=columns,
        key=f"{key_prefix}_select"
    )
    
    if selected_column:
        st.write(f"Preview of {column_type} column:")
        preview_data = df[selected_column].head()
        st.dataframe(
            pd.DataFrame({
                "Row": range(1, 6),
                f"{column_type}": preview_data
            }),
            hide_index=True
        )
    return selected_column

def render_upload_section():
    # Initialize session state variables if not exists
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'smiles_column' not in st.session_state:
        st.session_state.smiles_column = None
    if 'activity_column' not in st.session_state:
        st.session_state.activity_column = None

    st.header("Data Upload")
    
    upload_method = st.radio(
        "Choose upload method",
        ["Upload CSV", "Use predefined dataset"],
        help="Select how you want to provide your data"
    )

    if upload_method == "Upload CSV":
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=['csv'],
            help="File should contain SMILES and activity data columns"
        )
        
        if uploaded_file:
            try:
                df = DataProcessor.load_csv(uploaded_file)
                st.success("Data uploaded successfully!")
                
                # Column selection with improved UI
                st.subheader("Column Selection")
                st.info("Please select the appropriate columns for analysis")
                
                # SMILES column selection
                smiles_column = render_column_selector(df, "SMILES", "smiles_column")
                
                # Activity column selection
                st.markdown("---")
                activity_column = render_column_selector(df, "Activity", "activity_column")
                
                if smiles_column and activity_column:
                    st.session_state.uploaded_data = df.copy()
                    st.session_state.smiles_column = smiles_column
                    st.session_state.activity_column = activity_column
                    st.success("✅ Column selection complete!")
                    
                    # Dataset overview
                    st.subheader("Dataset Overview")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Compounds", len(df))
                    with col2:
                        st.metric("Number of Columns", len(df.columns))
                    
                    st.write("Preview of the dataset:")
                    st.dataframe(df.head(), use_container_width=True)
                
            except ValueError as e:
                st.error(str(e))
    
    else:
        datasets = DataProcessor.get_predefined_datasets()
        selected_dataset = st.selectbox(
            "Select a predefined dataset",
            list(datasets.keys()),
            help="Choose from our curated collection of chemical datasets"
        )
        
        # Create a placeholder for loading message
        loading_placeholder = st.empty()
        
        if st.button("Load Dataset", help="Click to load the selected dataset"):
            loading_placeholder.info("Loading dataset... Please wait.")
            try:
                df = DataProcessor.load_predefined_dataset(selected_dataset)
                loading_placeholder.success(f"Loaded {selected_dataset} dataset successfully!")
                
                # Column selection with improved UI
                st.subheader("Column Selection")
                st.info("Please select the appropriate columns for analysis")
                
                # SMILES column selection
                smiles_column = render_column_selector(df, "SMILES", "smiles_column_pred")
                
                # Activity column selection
                st.markdown("---")
                activity_column = render_column_selector(df, "Activity", "activity_column_pred")
                
                if smiles_column and activity_column:
                    st.session_state.uploaded_data = df.copy()
                    st.session_state.smiles_column = smiles_column
                    st.session_state.activity_column = activity_column
                    st.session_state.selected_dataset = selected_dataset
                    st.success("✅ Column selection complete!")
                    
                    # Dataset overview
                    st.subheader("Dataset Overview")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Compounds", len(df))
                    with col2:
                        st.metric("Number of Columns", len(df.columns))
                    
                    st.write("Preview of the dataset:")
                    st.dataframe(df.head(), use_container_width=True)
                    
            except Exception as e:
                loading_placeholder.error(f"Error loading dataset: {str(e)}")
