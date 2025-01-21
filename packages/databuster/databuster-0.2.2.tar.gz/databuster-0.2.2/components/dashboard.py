import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import plotly.express as px
from utils.chemical_analysis import ChemicalAnalyzer
from components.job_history import JobHistory

class MolecularDashboard:
    def __init__(self):
        if 'dashboard_preferences' not in st.session_state:
            st.session_state.dashboard_preferences = {
                'favorite_analyses': [],
                'chart_type': 'scatter',
                'descriptor_columns': [],
                'show_3d': False
            }
        self.job_history = JobHistory()

    def save_preferences(self):
        """Save current dashboard preferences to session state"""
        if st.session_state.get('new_favorites'):
            st.session_state.dashboard_preferences['favorite_analyses'] = st.session_state.new_favorites
        if st.session_state.get('chart_selection'):
            st.session_state.dashboard_preferences['chart_type'] = st.session_state.chart_selection

    def render_preferences_section(self):
        """Render the dashboard preferences section"""
        st.subheader("Dashboard Preferences")
        
        # Analysis type preferences
        st.multiselect(
            "Favorite Analysis Types",
            ["Duplicate Detection", "Chirality Analysis", "Salt Detection", 
             "Structure Standardization", "Molecular Descriptors"],
            key='new_favorites',
            default=st.session_state.dashboard_preferences['favorite_analyses'],
            help="Select your preferred analysis types to show on dashboard"
        )
        
        # Visualization preferences
        st.selectbox(
            "Preferred Chart Type",
            ["scatter", "box", "violin", "bar"],
            key='chart_selection',
            index=["scatter", "box", "violin", "bar"].index(
                st.session_state.dashboard_preferences['chart_type']
            ),
            help="Select your preferred chart type for visualizations"
        )

        if st.button("Save Preferences"):
            self.save_preferences()
            st.success("Preferences saved successfully!")

    def render_quick_insights(self):
        """Render quick insights section based on recent analyses"""
        if not st.session_state.get('analysis_results'):
            st.info("Run some analyses to see insights here!")
            return

        st.subheader("Quick Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if "Molecular Descriptors" in st.session_state.analysis_results:
                df = st.session_state.analysis_results["Molecular Descriptors"]
                if not df.empty:
                    # Create distribution plot of molecular weight
                    if 'MolecularWeight' in df.columns:
                        fig = px.histogram(
                            df, x='MolecularWeight',
                            title='Molecular Weight Distribution'
                        )
                        st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "Duplicate Detection" in st.session_state.analysis_results:
                duplicates = st.session_state.analysis_results["Duplicate Detection"]
                if duplicates:
                    st.metric(
                        "Duplicate Groups Found",
                        len(duplicates),
                        help="Number of compound groups with similar structures"
                    )

    def render_recent_analyses(self):
        """Render recent analyses section"""
        if not hasattr(st.session_state, 'job_history'):
            st.info("No recent analyses found")
            return

        st.subheader("Recent Analyses")
        
        for job in st.session_state.job_history[:5]:  # Show last 5 analyses
            with st.expander(f"Analysis from {job['timestamp']}"):
                st.write(f"Types: {', '.join(job['analysis_types'])}")
                st.progress(job['progress'])
                if job['status'] == 'completed':
                    st.success("Completed")
                elif job['status'] == 'failed':
                    st.error(f"Failed: {job['error']}")

def render_dashboard():
    """Main function to render the molecular dashboard"""
    st.title("Molecular Analysis Dashboard")
    
    dashboard = MolecularDashboard()
    
    # Create tabs for different dashboard sections
    tab1, tab2, tab3 = st.tabs(["Quick Insights", "Recent Analyses", "Preferences"])
    
    with tab1:
        dashboard.render_quick_insights()
    
    with tab2:
        dashboard.render_recent_analyses()
    
    with tab3:
        dashboard.render_preferences_section()

if __name__ == "__main__":
    render_dashboard()
