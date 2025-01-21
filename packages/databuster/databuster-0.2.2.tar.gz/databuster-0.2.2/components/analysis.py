import streamlit as st
from utils.chemical_analysis import ChemicalAnalyzer
from utils.api_handlers import ChEMBLHandler
import pandas as pd
from typing import List, Dict
import logging
import time
from components.job_history import JobHistory

def process_analysis(df: pd.DataFrame, analysis_types: List[str], smiles_column: str) -> Dict:
    """
    Process compounds with simplified analysis workflow
    """
    results = {}
    try:
        smiles_list = df[smiles_column].tolist()
        if not smiles_list:
            raise ValueError("No SMILES data found in the specified column")

        # Process each analysis type
        for analysis_type in analysis_types:
            if analysis_type == "Molecular Descriptors":
                descriptors = []
                for smiles in smiles_list:
                    desc = ChemicalAnalyzer.calculate_descriptors(smiles)
                    if desc:
                        desc["SMILES"] = smiles
                        descriptors.append(desc)
                if descriptors:
                    results["Molecular Descriptors"] = pd.DataFrame(descriptors)

            elif analysis_type == "Duplicate Detection":
                duplicates = ChemicalAnalyzer.identify_duplicates(smiles_list)
                if duplicates:
                    results[analysis_type] = duplicates

            elif analysis_type == "Chirality Analysis":
                chiral_compounds = [smiles for smiles in smiles_list 
                                 if ChemicalAnalyzer.detect_chirality(smiles)[0]]
                if chiral_compounds:
                    results[analysis_type] = chiral_compounds

            elif analysis_type == "Salt Detection":
                salt_compounds = [smiles for smiles in smiles_list 
                               if ChemicalAnalyzer.identify_salts(smiles)]
                if salt_compounds:
                    results[analysis_type] = salt_compounds

            elif analysis_type == "Others":
                # Process other molecular features
                results[analysis_type] = {
                    "peptide_like": [s for s in smiles_list if ChemicalAnalyzer.is_peptide_like(s)],
                    "macrocyclic": [s for s in smiles_list if ChemicalAnalyzer.is_macrocyclic(s)],
                    "sugar_like": [s for s in smiles_list if ChemicalAnalyzer.is_sugar_like(s)]
                }

        return results

    except Exception as e:
        logging.error(f"Error in analysis: {str(e)}")
        raise

def render_analysis_section():
    """Main function to render the analysis section"""
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.warning("Please upload data first!")
        return

    st.header("Analysis")

    # Initialize job history
    job_history = JobHistory()

    # Enhanced field selection UI with better organization
    st.subheader("Analysis Configuration")

    # Updated analysis type selection without Structure Standardization
    analysis_types = [
        "Duplicate Detection",
        "Chirality Analysis",
        "Salt Detection",
        "Molecular Descriptors",
        "Others"  # New category for peptide-like, macrocyclic, and sugar-like compounds
    ]

    st.session_state.analysis_types = st.multiselect(
        "Select Analysis Types",
        analysis_types,
        default=["Duplicate Detection", "Molecular Descriptors"],
        help="Choose one or more types of analysis to perform on your dataset"
    )

    # Show selected SMILES column
    st.info(f"SMILES Column: {st.session_state.get('smiles_column', 'Not selected')}")

    # Get dataframe
    df = st.session_state.uploaded_data

    if st.button("Run Analysis"):
        try:
            # Create new job in history
            job_id = job_history.add_job(st.session_state.analysis_types)

            # Initialize progress tracking
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()

            status_text.text("Running analysis...")
            results = process_analysis(df, st.session_state.analysis_types, st.session_state.smiles_column)

            # Update progress as analysis completes
            progress_bar.progress(1.0)
            status_text.text("Analysis completed")

            # Store results in session state
            st.session_state.analysis_results = results

            # Complete job and show results
            job_history.complete_job(job_id)
            progress_container.success("✅ Analysis completed successfully!")

            # Display results section
            if 'analysis_results' in st.session_state:
                from components.results import render_results_section
                render_results_section()

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            logging.error(f"Analysis error: {str(e)}")
            job_history.fail_job(job_id, str(e))