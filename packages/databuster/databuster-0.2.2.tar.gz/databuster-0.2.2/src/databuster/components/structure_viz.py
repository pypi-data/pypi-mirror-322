import streamlit as st
import py3Dmol
from rdkit import Chem
from rdkit.Chem import Descriptors, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
import base64
import io

def render_structure_viewer(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            st.error("Invalid SMILES string")
            return
            
        # Generate 2D coordinates for the molecule
        rdDepictor.Compute2DCoords(mol)
        
        # Convert to SDF for 3D view
        sdf = Chem.MolToMolBlock(mol)
        
        # Display SMILES and basic info
        st.code(smiles, language="text")
        
        # Display basic molecular information
        with st.expander("Structure Information"):
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.write("Formula:", Chem.rdMolDescriptors.CalcMolFormula(mol))
                st.write("Exact Mass:", f"{Descriptors.ExactMolWt(mol):.2f}")
            with info_col2:
                st.write("# Atoms:", mol.GetNumAtoms())
                st.write("# Bonds:", mol.GetNumBonds())
        
        # 3D Viewer
        st.subheader("3D Structure")
        viewer = py3Dmol.view(width=400, height=400)
        viewer.addModel(sdf, "sdf")
        viewer.setStyle({'stick':{}})
        viewer.zoomTo()
        
        # Display 3D viewer
        html = viewer.render()
        st.components.v1.html(html, height=400)
            
    except Exception as e:
        st.error(f"Error visualizing structure: {str(e)}")
