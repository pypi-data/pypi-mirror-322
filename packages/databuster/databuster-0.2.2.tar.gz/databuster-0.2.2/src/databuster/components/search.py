import streamlit as st
import pandas as pd
from utils.search_filters import CompoundSearcher
from typing import Dict, List, Optional
import numpy as np

def render_search_section():
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.warning("Please upload data first!")
        return

    st.header("Smart Search & Filter")
    
    # Initialize searcher
    searcher = CompoundSearcher()
    
    # Create tabs for different search types
    search_tabs = st.tabs([
        "Property Search",
        "Structural Features",
        "Similarity Search",
        "Substructure Search"
    ])
    
    # Property Search Tab
    with search_tabs[0]:
        st.subheader("Search by Property Ranges")
        
        col1, col2 = st.columns(2)
        property_ranges = {}
        
        with col1:
            # Molecular Weight Range
            st.write("Molecular Weight Range")
            mw_min = st.number_input("Min MW", value=0.0, step=50.0)
            mw_max = st.number_input("Max MW", value=1000.0, step=50.0)
            if mw_min < mw_max:
                property_ranges['MW'] = {'min': mw_min, 'max': mw_max}
        
        with col2:
            # LogP Range
            st.write("LogP Range")
            logp_min = st.number_input("Min LogP", value=-5.0, step=0.5)
            logp_max = st.number_input("Max LogP", value=5.0, step=0.5)
            if logp_min < logp_max:
                property_ranges['LogP'] = {'min': logp_min, 'max': logp_max}
        
        if st.button("Search by Properties"):
            if property_ranges:
                results = searcher.search_by_property_range(
                    st.session_state.uploaded_data,
                    property_ranges
                )
                if not results.empty:
                    st.write(f"Found {len(results)} compounds matching the criteria")
                    st.dataframe(results)
                    
                    # Download button for results
                    csv = results.to_csv(index=False)
                    st.download_button(
                        "Download Results",
                        csv,
                        "property_search_results.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No compounds found matching these criteria")
    
    # Structural Features Tab
    with search_tabs[1]:
        st.subheader("Search by Structural Features")
        
        available_features = list(searcher.smarts_patterns.keys())
        selected_features = st.multiselect(
            "Select structural features to search for",
            available_features,
            help="Select one or more structural features to find in compounds"
        )
        
        if st.button("Search by Features"):
            if selected_features:
                results = searcher.search_by_structural_features(
                    st.session_state.uploaded_data,
                    st.session_state.smiles_column,
                    selected_features
                )
                if not results.empty:
                    st.write(f"Found {len(results)} compounds with selected features")
                    st.dataframe(results)
                    
                    # Download button for results
                    csv = results.to_csv(index=False)
                    st.download_button(
                        "Download Results",
                        csv,
                        "structural_search_results.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No compounds found with these features")
    
    # Similarity Search Tab
    with search_tabs[2]:
        st.subheader("Search by Structural Similarity")
        
        query_smiles = st.text_input(
            "Enter SMILES for similarity search",
            help="Enter a SMILES string to find similar compounds"
        )
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05
        )
        
        if st.button("Search Similar Compounds"):
            if query_smiles:
                results = searcher.similarity_search(
                    st.session_state.uploaded_data,
                    query_smiles,
                    st.session_state.smiles_column,
                    similarity_threshold
                )
                if not results.empty:
                    st.write(f"Found {len(results)} similar compounds")
                    st.dataframe(results)
                    
                    # Download button for results
                    csv = results.to_csv(index=False)
                    st.download_button(
                        "Download Results",
                        csv,
                        "similarity_search_results.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No similar compounds found")
    
    # Substructure Search Tab
    with search_tabs[3]:
        st.subheader("Search by Substructure")
        
        query_smarts = st.text_input(
            "Enter SMARTS pattern for substructure search",
            help="Enter a SMARTS pattern to find compounds containing this substructure"
        )
        
        if st.button("Search Substructure"):
            if query_smarts:
                results = searcher.substructure_search(
                    st.session_state.uploaded_data,
                    query_smarts,
                    st.session_state.smiles_column
                )
                if not results.empty:
                    st.write(f"Found {len(results)} compounds containing the substructure")
                    st.dataframe(results)
                    
                    # Download button for results
                    csv = results.to_csv(index=False)
                    st.download_button(
                        "Download Results",
                        csv,
                        "substructure_search_results.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No compounds found containing this substructure")
