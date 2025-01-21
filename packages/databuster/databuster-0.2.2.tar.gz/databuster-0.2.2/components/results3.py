import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from utils.chemical_analysis import ChemicalAnalyzer
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalogParams, FilterCatalog

# Mapping of display names to RDKit descriptor functions
DESCRIPTOR_MAPPING = {
    "MW": Descriptors.ExactMolWt,
    "LogP": Descriptors.MolLogP,
    "TPSA": Descriptors.TPSA,
    "Random": None
}

def get_descriptor_value(mol, descriptor_name):
    """Safely get descriptor value using the mapping"""
    if descriptor_name == "Random":
        return None
    descriptor_func = DESCRIPTOR_MAPPING.get(descriptor_name)
    if descriptor_func and mol:
        try:
            return descriptor_func(mol)
        except:
            return None
    return None

# Function to compute PAINS alerts using RDKit's PAINS filter
def compute_pains_alerts(df, smiles_column):
    """Compute PAINS alerts and create a new column in the dataframe."""
    # Initialize PAINS filter
    params = FilterCatalogParams()
    params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
    catalog = FilterCatalog(params)

    pains_alerts = []
    for index, row in df.iterrows():
        mol = Chem.MolFromSmiles(row[smiles_column])
        if mol:
            entry = catalog.GetFirstMatch(mol)
            pains_alerts.append(entry is not None)  # True if PAINS is detected
        else:
            pains_alerts.append(False)
    
    df['PAINS_alert'] = pains_alerts
    return df

# Function to create a Streamlit select box for selecting the activity field
def select_activity_field(df):
    """Ask the user to select the activity field from the dataframe columns."""
    activity_field = st.selectbox("Select the Activity Field", df.columns)
    return activity_field

# Adding the PAINS bar plot after the Lipinski violation pie chart
def create_pains_alerts_bar_plot(df):
    """Create a bar plot for compounds with and without PAINS alerts."""
    if 'PAINS_alert' in df.columns and 'activity' in df.columns:
        # Count compounds with and without PAINS alerts
        pains_counts = df.groupby('PAINS_alert')['activity'].count().reset_index()
        pains_counts.columns = ['PAINS_alert', 'Compound Count']
        
        # Create the bar plot
        fig = px.bar(pains_counts, x='PAINS_alert', y='Compound Count', title='Compounds with and without PAINS Alerts')
        fig.update_layout(xaxis_title="PAINS Alert (Yes/No)", yaxis_title="Number of Compounds")
        
        return fig
    else:
        st.warning("PAINS alert or activity columns not found in the dataset.")
        return None
    
def create_property_distribution_plot(data, property_name):
    """Create a distribution plot for a given property"""
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=data,
        name=property_name,
        nbinsx=30,
        histnorm='probability density'
    ))
    
    # Add KDE if enough data points
    if len(data) > 1:
        kde_x = np.linspace(data.min(), data.max(), 100)
        kde = stats.gaussian_kde(data.dropna())
        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde(kde_x),
            mode='lines',
            name='KDE',
            line=dict(color='red')
        ))
    
    fig.update_layout(
        title=f'{property_name} Distribution',
        xaxis_title=property_name,
        yaxis_title='Density',
        showlegend=True
    )
    return fig

def display_molecular_statistics(df):
    """Display key molecular statistics"""
    st.subheader("Molecular Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Basic statistics
    with col1:
        st.metric("Average MW", f"{df['MW'].mean():.1f}")
    with col2:
        st.metric("Average LogP", f"{df['LogP'].mean():.1f}")
    with col3:
        st.metric("Average TPSA", f"{df['TPSA'].mean():.1f}")
    with col4:
        st.metric("Average Rotatable Bonds", f"{df['RotBonds'].mean():.1f}")

def render_structure_visualization(df, smiles_column):
    """Render chemical structure visualization section"""
    st.subheader("Structure Visualization")
    
    # Structure display options
    cols = st.columns([2, 1])
    with cols[0]:
        n_structures = st.slider("Number of structures to display", 
                               min_value=1, 
                               max_value=12, 
                               value=6)
    with cols[1]:
        sort_by = st.selectbox("Sort structures by",
                             list(DESCRIPTOR_MAPPING.keys()))
    
    try:
        # Get structures to display
        if sort_by == "Random":
            display_df = df.sample(n_structures)
        else:
            # Calculate descriptor values for sorting
            descriptor_values = []
            for smiles in df[smiles_column]:
                mol = Chem.MolFromSmiles(smiles)
                value = get_descriptor_value(mol, sort_by)
                descriptor_values.append(value if value is not None else float('nan'))
            
            temp_df = df.copy()
            temp_df['descriptor_value'] = descriptor_values
            temp_df = temp_df.dropna(subset=['descriptor_value'])
            
            display_df = pd.concat([
                temp_df.nsmallest(n_structures//2, 'descriptor_value'),
                temp_df.nlargest(n_structures//2, 'descriptor_value')
            ])
        
        # Create structure grid
        mols = [Chem.MolFromSmiles(smiles) for smiles in display_df[smiles_column]]
        legends = []
        for mol in mols:
            if sort_by == "Random" or not mol:
                legends.append("")
            else:
                value = get_descriptor_value(mol, sort_by)
                legends.append(f"{sort_by}: {value:.1f}" if value is not None else "")
        
        # Generate and display the grid
        img = Draw.MolsToGridImage(
            mols,
            molsPerRow=min(3, n_structures),
            subImgSize=(300, 300),
            legends=legends,
            returnPNG=False
        )
        st.image(img)
        
    except Exception as e:
        st.error(f"Error generating structure visualization: {str(e)}")

def create_lipinski_analysis(df):
    """Create Lipinski's Rule of Five analysis"""
    st.subheader("Lipinski's Rule of Five Analysis")
    
    # Calculate violations
    violations = {
        'MW > 500': df['MW'] > 500,
        'LogP > 5': df['LogP'] > 5,
        'HBD > 5': df['HBD'] > 5,
        'HBA > 10': df['HBA'] > 10
    }
    
    # Count total violations per compound
    total_violations = sum(violations.values())
    violation_counts = pd.Series(total_violations).value_counts().sort_index()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=[f"{i} violations" for i in violation_counts.index],
        values=violation_counts.values,
        hole=0.3
    )])
    
    fig.update_layout(title="Distribution of Lipinski Violations")
    
    return fig, violations

def create_property_correlation_plot(df):
    """Create correlation plot for molecular properties"""
    properties = ['MW', 'LogP', 'TPSA', 'HBA', 'HBD', 'RotBonds']
    available_properties = [prop for prop in properties if prop in df.columns]
    
    if not available_properties:
        st.warning("No molecular properties available for correlation plot")
        return None
        
    corr_matrix = df[available_properties].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    
    fig.update_layout(
        title='Property Correlations',
        width=700,
        height=700
    )
    return fig

def render_results_section():
    """Main function to render analysis results"""
    if not hasattr(st.session_state, 'uploaded_data') or st.session_state.uploaded_data is None:
        st.info("Please upload a dataset first.")
        return

    if not hasattr(st.session_state, 'analysis_results') or st.session_state.analysis_results is None:
        st.info("No analysis results available. Please run the analysis first.")
        return
        
    try:
        # Get results from session state
        results = getattr(st.session_state, 'analysis_results', {})
        
        # Display compound statistics
        st.header("Analysis Results")
        
        # Summary metrics
        total_compounds = len(st.session_state.uploaded_data)
        unique_compounds = len(set(st.session_state.uploaded_data[st.session_state.smiles_column]))
    except Exception as e:
        st.error(f"An error occurred while retrieving results: {e}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Compounds", str(total_compounds))
        with col2:
            st.metric("Unique Compounds", str(unique_compounds))
        with col3:
            st.metric("Duplicate Rate", f"{(1 - unique_compounds/total_compounds)*100:.1f}%")
        
        # Create tabs for different analysis sections
        tabs = st.tabs([
            "Molecular Properties",
            "Structure Analysis",
            "Property Distribution",
            "Drug-likeness"
        ])
        
        # Molecular Properties Tab
        with tabs[0]:
            if isinstance(results, dict) and "Molecular Descriptors" in results:
                desc_df = results["Molecular Descriptors"]
                display_molecular_statistics(desc_df)
                
                # Property correlation plot
                corr_plot = create_property_correlation_plot(desc_df)
                if corr_plot:
                    st.plotly_chart(corr_plot)
                
                # Download option
                csv = desc_df.to_csv(index=False)
                st.download_button(
                    "Download Descriptor Data",
                    csv,
                    "molecular_descriptors.csv",
                    "text/csv"
                )
        
        # Structure Analysis Tab     
        # Property Distribution Tab
        with tabs[1]:
            if isinstance(results, dict) and "Molecular Descriptors" in results:
                desc_df = results["Molecular Descriptors"]
                properties = ['MW', 'LogP', 'TPSA', 'HBA', 'HBD', 'RotBonds']
                
                selected_property = st.selectbox(
                    "Select property to visualize",
                    properties
                )
                
                st.plotly_chart(
                    create_property_distribution_plot(
                        desc_df[selected_property],
                        selected_property
                    )
                )
                
        with tabs[2]:
            if st.session_state.smiles_column:
                render_structure_visualization(
                    st.session_state.uploaded_data,
                    st.session_state.smiles_column
                )
                
                # Structure flags
                st.subheader("Structure Analysis")
                flag_col1, flag_col2, flag_col3 = st.columns(3)
                
                with flag_col1:
                    if isinstance(results, dict) and "Salt Detection" in results:
                        salt_count = len(results["Salt Detection"])
                        st.metric("Compounds with Salts", 
                                f"{salt_count}",
                                f"{(salt_count/total_compounds)*100:.1f}%")
                
                with flag_col2:
                    if isinstance(results, dict) and "Chirality Analysis" in results:
                        chiral_count = len(results["Chirality Analysis"])
                        st.metric("Chiral Compounds",
                                f"{chiral_count}",
                                f"{(chiral_count/total_compounds)*100:.1f}%")
                
                with flag_col3:
                    if isinstance(results, dict) and "Duplicate Detection" in results:
                        dup_count = sum(len(indices) for indices in results["Duplicate Detection"].values())
                        st.metric("Duplicate Structures",
                                f"{dup_count}",
                                f"{(dup_count/total_compounds)*100:.1f}%")
        # Drug-likeness Tab
        # Drug-likeness Tab
        with tabs[3]:
            # Define the function outside the "with tabs[3]:" block
            def display_drug_likeness_tab(results):
                """Display the Drug-likeness tab with Lipinski violations and PAINS alert analysis."""
                if isinstance(results, dict):
                    # Ensure original fields and computed descriptors are combined
                    if "Original Data" in results and "Molecular Descriptors" in results:
                        original_df = results["Original Data"]  # Contains SMILES, activity, etc.
                        desc_df = results["Molecular Descriptors"]  # Computed molecular properties

                        # Merge original and computed data
                        combined_df = pd.concat([original_df, desc_df], axis=1)

                        # Ask user for SMILES column and compute PAINS alerts
                        smiles_column = st.selectbox("Select the SMILES Column", combined_df.columns)
                        combined_df = compute_pains_alerts(combined_df, smiles_column)

                        # Ask user for activity field
                        activity_field = select_activity_field(combined_df)

                        # Lipinski violations pie chart
                        lipinski_plot, violations = create_lipinski_analysis(combined_df)
                        st.plotly_chart(lipinski_plot)

                        # Adding PAINS alerts bar plot with activity field mapping
                        pains_plot = create_pains_alerts_bar_plot(combined_df[[activity_field, 'PAINS_alert']])
                        if pains_plot:
                            st.plotly_chart(pains_plot)
                    else:
                        st.error("Original data or computed descriptors are missing in the results.")
            
                    # Now, call the function inside the tab
                #display_drug_likeness_tab(results)

if __name__ == "__main__":
    st.set_page_config(page_title="Chemical Analysis Results", layout="wide")
    render_results_section()