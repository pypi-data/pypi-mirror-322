from chembl_webresource_client.new_client import new_client
from typing import Dict, List
import pandas as pd

class ChEMBLHandler:
    def __init__(self):
        self.molecule = new_client.molecule
        self.similarity = new_client.similarity

    def search_compound(self, smiles: str) -> Dict:
        try:
            results = self.similarity.filter(smiles=smiles, similarity=85)
            return [r for r in results]
        except Exception as e:
            return {"error": str(e)}

    def get_compound_details(self, chembl_id: str) -> Dict:
        try:
            return self.molecule.get(chembl_id)
        except Exception as e:
            return {"error": str(e)}
