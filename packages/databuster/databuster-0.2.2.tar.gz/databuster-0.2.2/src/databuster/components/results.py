import logging
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from rdkit import Chem
from rdkit.Chem import Descriptors, rdDepictor
from rdkit.Chem.FilterCatalog import FilterCatalogParams, FilterCatalog
import requests
import io
from utils.chemical_analysis import ChemicalAnalyzer
import requests
import io
import mols2grid
import tempfile
from rdkit import Chem
from rdkit.Chem import AllChem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        except Exception:
            return None
    return None


def create_complete_analysis_df(results, uploaded_data, smiles_column):
    """Create a comprehensive DataFrame containing all analysis results"""
    # Start with the original uploaded data
    complete_df = uploaded_data.copy()

    # Add molecular descriptors if available
    if "Molecular Descriptors" in results:
        desc_df = results["Molecular Descriptors"]
        # Merge with original data using SMILES column
        complete_df = complete_df.merge(desc_df.drop(columns=[smiles_column],
                                                     errors='ignore'),
                                        left_on=smiles_column,
                                        right_on='SMILES',
                                        how='left')

    # Process peptide and macrocyclic detection
    complete_df = detect_peptide_like(complete_df, smiles_column)
    complete_df = detect_macrocyclic_like(complete_df, smiles_column)
    complete_df = detect_sugar_like(complete_df, smiles_column)

    # Add chiral information
    if "Chirality Analysis" in results:
        complete_df = ChemicalAnalyzer.process_chirality_info(complete_df, smiles_column)

    # Add PAINS alerts
    complete_df = compute_pains_alerts(complete_df, smiles_column)

    # Add duplicate information
    if "Duplicate Detection" in results:
        duplicates = results["Duplicate Detection"]

        # Initialize duplicate columns
        complete_df['Has_Exact_Duplicates'] = False
        complete_df['Has_Desalted_Duplicates'] = False
        complete_df['Has_Similar_Duplicates'] = False
        complete_df['Exact_Duplicate_Group'] = None
        complete_df['Desalted_Duplicate_Group'] = None
        complete_df['Similar_Duplicate_Group'] = None
        complete_df['Exact_Duplicate_Group_Size'] = 0
        complete_df['Desalted_Duplicate_Group_Size'] = 0
        complete_df['Similar_Duplicate_Group_Size'] = 0

        # Process each type of duplicate
        for dup_type in ['exact', 'desalted', 'similar']:
            if dup_type in duplicates:
                type_duplicates = duplicates[dup_type]

                # Mark compounds that have duplicates
                for group_id, indices in type_duplicates.items():
                    group_size = len(indices)
                    for idx in indices:
                        try:
                            smiles = uploaded_data.iloc[idx][smiles_column]
                            complete_df.loc[complete_df[smiles_column] == smiles, f'Has_{dup_type.capitalize()}_Duplicates'] = True
                            complete_df.loc[complete_df[smiles_column] == smiles, f'{dup_type.capitalize()}_Duplicate_Group'] = f"group_{group_id}"
                            complete_df.loc[complete_df[smiles_column] == smiles, f'{dup_type.capitalize()}_Duplicate_Group_Size'] = group_size
                        except IndexError:
                            continue

    return complete_df


# Function to compute PAINS alerts using RDKit's PAINS filter
def compute_pains_alerts(df, smiles_column):
    """Compute PAINS alerts and create a new column in the dataframe."""
    # Initialize PAINS filter
    params = FilterCatalogParams()
    params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
    catalog = FilterCatalog(params)

    pains_alerts = []
    pains_tags = []
    for index, row in df.iterrows():
        mol = Chem.MolFromSmiles(row[smiles_column])
        if mol:
            entry = catalog.GetFirstMatch(mol)
            if entry:
                pains_alerts.append(True)
                pains_tags.append(entry.GetDescription())
            else:
                pains_alerts.append(False)
                pains_tags.append(None)
        else:
            pains_alerts.append(False)
            pains_tags.append(None)

    df['PAINS_alert'] = pains_alerts
    df['PAINS_tag'] = pains_tags
    return df


# Function to create a Streamlit select box for selecting the activity field
def select_activity_field(df):
    """Ask the user to select the activity field from the dataframe columns."""
    activity_field = st.selectbox("Select the Activity Field",
                                  df.columns,
                                  key="activity_field_selectbox")
    return activity_field


# Adding the PAINS bar plot after the Lipinski violation pie chart
def create_pains_alerts_bar_plot(df):
    """Create a bar plot for compounds with and without PAINS alerts."""
    if 'PAINS_alert' in df.columns:
        # Count compounds with and without PAINS alerts
        pains_counts = df['PAINS_alert'].value_counts().reset_index()
        pains_counts.columns = ['PAINS_alert', 'Compound Count']

        # Create the bar plot
        fig = px.bar(pains_counts,
                     x='PAINS_alert',
                     y='Compound Count',
                     title='Compounds with and without PAINS Alerts')
        fig.update_layout(xaxis_title="PAINS Alert (Yes/No)",
                          yaxis_title="Number of Compounds")

        return fig
    else:
        st.warning("PAINS alert column not found in the dataset.")
        return None


def create_property_distribution_plot(data, property_name):
    """Create a distribution plot for a given property"""
    fig = go.Figure()

    # Add histogram
    fig.add_trace(
        go.Histogram(x=data,
                     name=property_name,
                     nbinsx=30,
                     histnorm='probability density'))

    # Add KDE if enough data points
    if len(data) > 1:
        kde_x = np.linspace(data.min(), data.max(), 100)
        kde = stats.gaussian_kde(data.dropna())
        fig.add_trace(
            go.Scatter(x=kde_x,
                       y=kde(kde_x),
                       mode='lines',
                       name='KDE',
                       line=dict(color='red')))

    fig.update_layout(title=f'{property_name} Distribution',
                      xaxis_title=property_name,
                      yaxis_title='Density',
                      showlegend=True)
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
    """Render chemical structure visualization section using PubChem API"""
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
                descriptor_values.append(
                    value if value is not None else float('nan'))

            temp_df = df.copy()
            temp_df['descriptor_value'] = descriptor_values
            temp_df = temp_df.dropna(subset=['descriptor_value'])

            display_df = pd.concat([
                temp_df.nsmallest(n_structures // 2, 'descriptor_value'),
                temp_df.nlargest(n_structures // 2, 'descriptor_value')
            ])

        # Create structure grid using HTML
        cols = st.columns(3)
        for idx, (_, row) in enumerate(display_df.iterrows()):
            mol = Chem.MolFromSmiles(row[smiles_column])
            if mol:
                # Generate SVG instead of PNG
                from rdkit.Chem import rdDepictor
                from rdkit.Chem.Draw import rdMolDraw2D

                # Compute 2D coordinates if needed
                rdDepictor.Compute2DCoords(mol)

                # Get structure image from PubChem
                img_url = ChemicalAnalyzer.get_structure_from_pubchem(
                    Chem.MolToSmiles(mol))
                if img_url:
                    structure_html = f'<img src="{img_url}" width="300" height="300" style="background-color: white;">'
                else:
                    structure_html = '<p>Structure not available</p>'

                # Add property information
                prop_info = [
                    f"MW: {Descriptors.ExactMolWt(mol):.1f}",
                    f"LogP: {Descriptors.MolLogP(mol):.1f}",
                    f"TPSA: {Descriptors.TPSA(mol):.1f}",
                    f"HBD: {Descriptors.NumHDonors(mol)}",
                    f"HBA: {Descriptors.NumHAcceptors(mol)}",
                    f"Rotatable Bonds: {Descriptors.NumRotatableBonds(mol)}"
                ]

                with cols[idx % 3]:
                    st.markdown(f"""
                        <div style="text-align: center;">
                            {structure_html}
                            <div style="font-size: 0.8em; margin-top: 5px;">
                                {'<br>'.join(prop_info)}
                            </div>
                        </div>
                    """,
                                unsafe_allow_html=True)
            else:
                with cols[idx % 3]:
                    st.error("Invalid structure")

    except Exception as e:
        st.error(f"Error generating structure visualization: {str(e)}")
        st.error(f"Detailed error: {str(e.__class__.__name__)}")


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
    fig = go.Figure(data=[
        go.Pie(labels=[f"{i} violations" for i in violation_counts.index],
               values=violation_counts.values,
               hole=0.3)
    ])

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

    fig = go.Figure(data=go.Heatmap(z=corr_matrix.values,
                                    x=corr_matrix.columns,
                                    y=corr_matrix.columns,
                                    colorscale='RdBu',
                                    zmin=-1,
                                    zmax=1))

    fig.update_layout(title='Property Correlations', width=700, height=700)
    return fig


def detect_peptide_like(df, smiles_column):
    """Detect peptide-like compounds based on certain criteria."""
    peptide_like = []
    for smiles in df[smiles_column]:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            # Example criteria: contains peptide bonds (C(=O)N)
            if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)N')):
                peptide_like.append(True)
            else:
                peptide_like.append(False)
        else:
            peptide_like.append(False)
    df['Peptide_like'] = peptide_like
    return df


def detect_macrocyclic_like(df, smiles_column):
    """Detect macrocyclic-like compounds based on certain criteria."""
    macrocyclic_like = []
    for smiles in df[smiles_column]:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            # Example criteria: contains a ring with more than 8 members
            if any(len(ring) > 8 for ring in mol.GetRingInfo().AtomRings()):
                macrocyclic_like.append(True)
            else:
                macrocyclic_like.append(False)
        else:
            macrocyclic_like.append(False)
    df['Macrocyclic_like'] = macrocyclic_like
    return df


def detect_sugar_like(df, smiles_column):
    """Detect sugar-like compounds (placeholder - needs a proper implementation)."""
    # This is a placeholder, replace with actual sugar detection logic
    sugar_like = [False] * len(df)
    df['Sugar_like'] = sugar_like
    return df


def download_complete_csv(df):
    """Download a complete CSV with all properties created during the analysis."""
    csv = df.to_csv(index=False)
    st.download_button("Download Complete Updated Data", csv,
                       "complete_updated.csv", "text/csv")


def check_valid_smiles(smiles):
    """Check if SMILES string is valid"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except:
        return False


def display_percentage_metric(label, count, total, threshold=15.0, inverse_colors=False):
    """Display metric with arrow based on percentage threshold"""
    percentage = (count / total * 100) if total > 0 else 0

    if inverse_colors:
        # For metrics where high percentage is good (like valid SMILES)
        delta_color = "normal" if percentage > 90 else "off" if percentage > 70 else "inverse"
    else:
        # For metrics where low percentage is preferred
        if percentage < 1.0:
            delta_color = "normal"  # Green down arrow for very low percentages
        elif percentage > threshold:
            delta_color = "inverse"  # Red up arrow for high percentages
        else:
            delta_color = "off"  # Neutral for middle range

    st.metric(
        label,
        f"{count}",
        f"{percentage:.1f}%",
        delta_color=delta_color
    )


def create_mols2grid_view(smiles_list, subset=None):
    """Create a mols2grid view for a list of SMILES"""
    if not smiles_list:
        return None

    # Create a DataFrame with SMILES
    df = pd.DataFrame({'SMILES': smiles_list})

    # Generate 2D coordinates for better visualization
    mols = [Chem.MolFromSmiles(s) for s in smiles_list]
    for mol in mols:
        if mol is not None:
            AllChem.Compute2DCoords(mol)

    # Create the mols2grid view
    return mols2grid.display(df,
                           smiles_col='SMILES',
                           subset=subset,
                           n_cols=4,
                           size=(200, 200),
                           properties=['SMILES'])


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

        # Create comprehensive analysis DataFrame
        complete_df = create_complete_analysis_df(results, st.session_state.uploaded_data, st.session_state.smiles_column)

        # Add group size information for duplicates
        if "Duplicate Detection" in results:
            duplicates = results["Duplicate Detection"]

            # Add columns for group sizes
            complete_df['Exact_Duplicate_Group_Size'] = 0
            complete_df['Desalted_Duplicate_Group_Size'] = 0
            complete_df['Similar_Duplicate_Group_Size'] = 0

            # Process each type of duplicate
            for dup_type in ['exact', 'desalted', 'similar']:
                if dup_type in duplicates:
                    for group_id, indices in duplicates[dup_type].items():
                        group_size = len(indices)
                        for idx in indices:
                            smiles = st.session_state.uploaded_data.iloc[idx][st.session_state.smiles_column]
                            complete_df.loc[complete_df[st.session_state.smiles_column] == smiles,
                                             f'{dup_type.capitalize()}_Duplicate_Group_Size'] = group_size

        # Store the complete analysis results in session state
        if 'complete_analysis_results' not in st.session_state:
            st.session_state.complete_analysis_results = complete_df

        # Add download button at the top
        csv_data = complete_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Complete Analysis Results",
            data=csv_data,
            file_name="complete_analysis_results.csv",
            mime="text/csv",
            help="Download all analysis results including molecular properties, stereochemistry, duplicates, and salts",
            key='download_complete_results'
        )

        # Display compound statistics
        st.header("Analysis Results")

        # Calculate metrics
        total_compounds = len(st.session_state.uploaded_data)
        unique_compounds = len(set(st.session_state.uploaded_data[st.session_state.smiles_column]))
        duplicate_rate = (1 - unique_compounds / total_compounds) * 100 if total_compounds > 0 else 0

        # Count valid SMILES
        valid_smiles_count = sum(check_valid_smiles(smiles) for smiles in st.session_state.uploaded_data[st.session_state.smiles_column])

        # Process detection results
        complete_df = detect_peptide_like(complete_df, st.session_state.smiles_column)
        complete_df = detect_macrocyclic_like(complete_df, st.session_state.smiles_column)
        complete_df = detect_sugar_like(complete_df, st.session_state.smiles_column)

        # Count compounds with specific properties
        peptide_count = complete_df['Peptide_like'].sum()
        macrocyclic_count = complete_df['Macrocyclic_like'].sum()
        sugar_count = complete_df['Sugar_like'].sum()

        # Count chiral compounds with specified stereochemistry
        chiral_with_stereo = sum(1 for _, row in complete_df.iterrows()
                                   if 'Stereo' in row and row['Stereo'] == 'Yes')

        # Count compounds with salts
        compounds_with_salts = sum(1 for smiles in st.session_state.uploaded_data[st.session_state.smiles_column]
                                   if ChemicalAnalyzer.identify_salts(smiles))

        # Display metrics in columns (2 rows of 4 columns)
        col1, col2, col3, col4 = st.columns(4)

        # First row
        with col1:
            st.metric("Total Compounds", str(total_compounds))  # No arrow needed

        with col2:
            display_percentage_metric("Valid SMILES", valid_smiles_count, total_compounds, inverse_colors=True)

        with col3:
            display_percentage_metric("Compounds with Salts", compounds_with_salts, total_compounds)

        with col4:
            display_percentage_metric("Chiral (Specified)", chiral_with_stereo, total_compounds)

        # Second row
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            display_percentage_metric("Macrocyclic-like", macrocyclic_count, total_compounds)

        with col6:
            display_percentage_metric("Peptide-like", peptide_count, total_compounds)

        with col7:
            display_percentage_metric("Sugar-like", sugar_count, total_compounds)

        with col8:
            display_percentage_metric("Duplicate Rate", total_compounds - unique_compounds, total_compounds)

        # Create updated tabs for different analysis sections
        tabs = st.tabs([
            "About Databuster",
            "Molecular Properties",
            "Drug-like",
            "Duplicates & Salts",
            "Other Observations"
        ])

        # Molecular Properties Tab
        with tabs[0]:
            st.write(
                "Databuster is a web-based tool for analyzing chemical datasets."
            )
            st.write(
                "It provides a range of features to analyze molecular properties, structure analysis, property distribution, duplicate detection, and salt detection."
            )
            st.image("DataBuster_LandingImage.png")  # , width=200)

        with tabs[1]:
            if isinstance(results,
                          dict) and "Molecular Descriptors" in results:
                desc_df = results["Molecular Descriptors"]
                if not desc_df.empty:
                    display_molecular_statistics(desc_df)

                    # Display all property distribution plots, 2 per row
                    properties = [
                        'MW', 'LogP', 'TPSA', 'HBA', 'HBD', 'RotBonds'
                    ]
                    rows = len(properties) // 2 + len(properties) % 2
                    for i in range(rows):
                        cols = st.columns(2)
                        for j in range(2):
                            index = i * 2 + j
                            if index < len(properties):
                                property_name = properties[index]
                                with cols[j]:
                                    st.plotly_chart(
                                        create_property_distribution_plot(
                                            desc_df[property_name],
                                            property_name),
                                        key=f'{property_name}_dist_plot')

                    # Property correlation plot
                    corr_plot = create_property_correlation_plot(desc_df)
                    if corr_plot:
                        st.plotly_chart(corr_plot, key='corr_plot')

                    # Download option
                    csv = desc_df.to_csv(index=False)
                    st.download_button("Download Descriptor Data", csv,
                                       "molecular_descriptors.csv", "text/csv")

                    # Download option for complete updated data
                    download_complete_csv(desc_df)
                else:
                    st.error("Molecular Descriptors data is empty.")
            else:
                st.error(
                    "Molecular Descriptors data is missing in the results.")

        # Drug-like Tab
        with tabs[2]:
            st.subheader("Drug-like Compounds Analysis")

            # Add mols2grid view for drug-like compounds
            drug_like_smiles = [smiles for smiles in complete_df[st.session_state.smiles_column]
                                if ChemicalAnalyzer.is_drug_like(smiles)]
            if drug_like_smiles:
                st.write(f"Found {len(drug_like_smiles)} drug-like compounds")
                grid_view = create_mols2grid_view(drug_like_smiles)
                if grid_view:
                    st.write(grid_view)

        # Duplicates & Salts Tab
        with tabs[3]:
            st.subheader("Duplicate Analysis")

            if "Duplicate Detection" in results:
                duplicates = results["Duplicate Detection"]

                # Create three columns for different duplicate types
                dup_col1, dup_col2, dup_col3 = st.columns(3)

                with dup_col1:
                    if 'exact' in duplicates:
                        st.write("### Exact Duplicates")
                        exact_df = pd.DataFrame({
                            'SMILES': [st.session_state.uploaded_data.iloc[idx][st.session_state.smiles_column]
                                       for group in duplicates['exact'].values()
                                       for idx in group],
                            'Group_Size': [len(group) for group in duplicates['exact'].values()
                                           for _ in range(len(group))]
                        })
                        st.dataframe(exact_df)

                with dup_col2:
                    if 'desalted' in duplicates:
                        st.write("### Desalted Duplicates")
                        desalted_df = pd.DataFrame({
                            'SMILES': [st.session_state.uploaded_data.iloc[idx][st.session_state.smiles_column]
                                       for group in duplicates['desalted'].values()
                                       for idx in group],
                            'Group_Size': [len(group) for group in duplicates['desalted'].values()
                                           for _ in range(len(group))]
                        })
                        st.dataframe(desalted_df)

                with dup_col3:
                    if 'similar' in duplicates:
                        st.write("### Similar Compounds")
                        similar_df = pd.DataFrame({
                            'SMILES': [st.session_state.uploaded_data.iloc[idx][st.session_state.smiles_column]
                                       for group in duplicates['similar'].values()
                                       for idx in group],
                            'Group_Size': [len(group) for group in duplicates['similar'].values()
                                           for _ in range(len(group))]
                        })
                        st.dataframe(similar_df)

            # Salt Analysis Section
            st.subheader("Salt Analysis")
            if "Salt Detection" in results:
                salt_compounds = results["Salt Detection"]
                if salt_compounds:
                    st.write(f"Found {len(salt_compounds)} compounds with salts")
                    salt_df = pd.DataFrame({'SMILES': salt_compounds})
                    grid_view = create_mols2grid_view(salt_compounds)
                    if grid_view:
                        st.write(grid_view)

        # Other Observations Tab
        with tabs[4]:
            st.subheader("Other Molecular Features")

            if "Others" in results:
                # Peptide-like compounds
                st.write("### Peptide-like Compounds")
                peptide_smiles = results["Others"]["peptide_like"]
                if peptide_smiles:
                    st.write(f"Found {len(peptide_smiles)} peptide-like compounds")
                    grid_view = create_mols2grid_view(peptide_smiles)
                    if grid_view:
                        st.write(grid_view)

                # Macrocyclic compounds
                st.write("### Macrocyclic Compounds")
                macro_smiles = results["Others"]["macrocyclic"]
                if macro_smiles:
                    st.write(f"Found {len(macro_smiles)} macrocyclic compounds")
                    grid_view = create_mols2grid_view(macro_smiles)
                    if grid_view:
                        st.write(grid_view)

                # Sugar-like compounds
                st.write("### Sugar-like Compounds")
                sugar_smiles = results["Others"]["sugar_like"]
                if sugar_smiles:
                    st.write(f"Found {len(sugar_smiles)} sugar-like compounds")
                    grid_view = create_mols2grid_view(sugar_smiles)
                    if grid_view:
                        st.write(grid_view)

    except Exception as e:
        st.error(f"Error rendering results: {str(e)}")
        logging.error(f"Results rendering error: {str(e)}")


if __name__ == "__main__":
    st.set_page_config(page_title="Chemical Analysis Results", layout="wide")
    render_results_section()