import streamlit as st
from datetime import datetime
import pandas as pd
import json
import uuid
from typing import Dict, List, Optional
import logging

class JobHistory:
    def __init__(self):
        if 'job_history' not in st.session_state:
            st.session_state.job_history = []
        
    def add_job(self, analysis_types: List[str]) -> str:
        """Add a new job to history and return its ID"""
        job_id = str(uuid.uuid4())
        job = {
            'id': job_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'running',
            'analysis_types': analysis_types,
            'progress': 0.0,
            'results_path': None,
            'error': None
        }
        st.session_state.job_history.insert(0, job)  # Add to start of list
        return job_id

    def update_job_progress(self, job_id: str, progress: float, status: str = 'running'):
        """Update job progress"""
        for job in st.session_state.job_history:
            if job['id'] == job_id:
                job['progress'] = progress
                job['status'] = status
                break

    def complete_job(self, job_id: str, results_path: Optional[str] = None):
        """Mark job as complete"""
        for job in st.session_state.job_history:
            if job['id'] == job_id:
                job['status'] = 'completed'
                job['progress'] = 1.0
                job['results_path'] = results_path
                break

    def fail_job(self, job_id: str, error_message: str):
        """Mark job as failed"""
        for job in st.session_state.job_history:
            if job['id'] == job_id:
                job['status'] = 'failed'
                job['error'] = error_message
                break

def render_job_history():
    """Render the job history timeline"""
    if not st.session_state.job_history:
        st.info("No analysis jobs run yet")
        return

    st.subheader("Analysis History")
    
    # Create columns for the timeline
    for job in st.session_state.job_history:
        with st.expander(f"Analysis Run - {datetime.fromisoformat(job['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"):
            # Show job details
            st.write(f"**Analysis Types:** {', '.join(job['analysis_types'])}")
            
            # Show status with appropriate color
            status_color = {
                'running': 'blue',
                'completed': 'green',
                'failed': 'red'
            }.get(job['status'], 'gray')
            
            st.markdown(f"**Status:** :{status_color}[{job['status'].upper()}]")
            
            # Show progress bar for running jobs
            if job['status'] == 'running':
                st.progress(job['progress'])
                
            # Show error if failed
            if job['status'] == 'failed' and job['error']:
                st.error(f"Error: {job['error']}")
                
            # Show download button for completed jobs with results
            if job['status'] == 'completed' and job['results_path']:
                try:
                    with open(job['results_path'], 'r') as f:
                        csv_data = f.read()
                    st.download_button(
                        label="⬇️ Download Results",
                        data=csv_data,
                        file_name=f"analysis_results_{datetime.fromisoformat(job['timestamp']).strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error loading results: {str(e)}")

# Initialize job history in session state
if 'job_history' not in st.session_state:
    st.session_state.job_history = []
