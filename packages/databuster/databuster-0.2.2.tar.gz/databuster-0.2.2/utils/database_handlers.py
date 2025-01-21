import requests
from typing import Dict, List, Optional
import pandas as pd
from rdkit import Chem
import json

class PubChemHandler:
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    
    @staticmethod
    def search_compound(smiles: str) -> Dict:
        """Search compound information from PubChem using SMILES"""
        try:
            # Convert SMILES to InChIKey for searching
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return {"error": "Invalid SMILES"}
                
            inchikey = Chem.MolToInchiKey(mol)
            
            # Search PubChem using InChIKey
            search_url = f"{PubChemHandler.BASE_URL}/compound/inchikey/{inchikey}/JSON"
            response = requests.get(search_url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "pubchem_cid": data["PC_Compounds"][0]["id"]["id"]["cid"],
                    "molecular_formula": data["PC_Compounds"][0].get("props", [{}])[0].get("value", {}).get("sval", ""),
                    "exact_mass": data["PC_Compounds"][0].get("props", [{}])[1].get("value", {}).get("sval", ""),
                    "source": "PubChem"
                }
            return {"error": f"No data found (Status: {response.status_code})"}
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_property_data(cid: int) -> Dict:
        """Get additional property data for a compound by CID"""
        try:
            property_url = f"{PubChemHandler.BASE_URL}/compound/cid/{cid}/property/MolecularWeight,XLogP,RotatableBondCount,HBondDonorCount,HBondAcceptorCount,TopologicalPolarSurfaceArea/JSON"
            response = requests.get(property_url)
            
            if response.status_code == 200:
                data = response.json()
                return data["PropertyTable"]["Properties"][0]
            return {"error": f"No property data found (Status: {response.status_code})"}
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def batch_search_compounds(smiles_list: List[str], batch_size: int = 50) -> pd.DataFrame:
        """Search multiple compounds and return results as a DataFrame"""
        results = []
        
        for i in range(0, len(smiles_list), batch_size):
            batch = smiles_list[i:i + batch_size]
            for smiles in batch:
                compound_data = PubChemHandler.search_compound(smiles)
                if "error" not in compound_data:
                    # Get additional property data
                    prop_data = PubChemHandler.get_property_data(compound_data["pubchem_cid"])
                    if "error" not in prop_data:
                        compound_data.update(prop_data)
                    
                compound_data["SMILES"] = smiles
                results.append(compound_data)
                
        return pd.DataFrame(results)

def compare_with_databases(smiles_list: List[str], batch_size: int = 50) -> Dict[str, pd.DataFrame]:
    """Compare input compounds with public databases"""
    results = {}
    
    # Get PubChem data
    pubchem_data = PubChemHandler.batch_search_compounds(smiles_list, batch_size)
    if not pubchem_data.empty:
        results["PubChem"] = pubchem_data
        
    return results
