from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
from typing import List, Dict, Union, Optional
import pandas as pd
import numpy as np
from utils.chemical_analysis import ChemicalAnalyzer

class CompoundSearcher:
    def __init__(self):
        self.smarts_patterns = {
            'aromatic': '[a]',
            'alcohol': '[OH]',
            'amine': '[NH2]',
            'carboxylic_acid': '[CH,CH2,CH3,CH4][CX3](=O)[OX2H1]',
            'ester': '[#6][CX3](=O)[OX2H0][#6]',
            'amide': '[NX3][CX3](=[OX1])[#6]',
            'sulfonamide': '[NX3][SX4](=[OX1])(=[OX1])[#6]',
            'phosphate': '[PX4](=[OX1])([OX2][#6])',
            'halogen': '[F,Cl,Br,I]'
        }

    def search_by_property_range(self, df: pd.DataFrame, 
                               property_ranges: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """
        Search compounds by property ranges
        
        Args:
            df: DataFrame containing compound data
            property_ranges: Dict of property ranges, e.g., 
                           {'MW': {'min': 200, 'max': 500},
                            'LogP': {'min': -1, 'max': 5}}
        """
        result_df = df.copy()
        for prop, range_dict in property_ranges.items():
            if prop in df.columns:
                if 'min' in range_dict:
                    result_df = result_df[result_df[prop] >= range_dict['min']]
                if 'max' in range_dict:
                    result_df = result_df[result_df[prop] <= range_dict['max']]
        return result_df

    def search_by_structural_features(self, df: pd.DataFrame, 
                                    smiles_column: str,
                                    features: List[str]) -> pd.DataFrame:
        """
        Search compounds by structural features using SMARTS patterns
        """
        def has_feature(smiles: str, pattern: str) -> bool:
            try:
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    return mol.HasSubstructMatch(Chem.MolFromSmarts(pattern))
                return False
            except:
                return False

        result_df = df.copy()
        for feature in features:
            if feature in self.smarts_patterns:
                mask = result_df[smiles_column].apply(
                    lambda x: has_feature(x, self.smarts_patterns[feature]))
                result_df[f'has_{feature}'] = mask
                result_df = result_df[mask]
        
        return result_df

    def similarity_search(self, df: pd.DataFrame,
                         query_smiles: str,
                         smiles_column: str,
                         threshold: float = 0.7) -> pd.DataFrame:
        """
        Search compounds by structural similarity using Morgan fingerprints
        """
        try:
            query_mol = Chem.MolFromSmiles(query_smiles)
            if not query_mol:
                return pd.DataFrame()

            query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2)
            
            def calculate_similarity(smiles: str) -> float:
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    if mol:
                        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
                        return DataStructs.TanimotoSimilarity(query_fp, fp)
                    return 0.0
                except:
                    return 0.0

            result_df = df.copy()
            result_df['similarity'] = result_df[smiles_column].apply(calculate_similarity)
            result_df = result_df[result_df['similarity'] >= threshold]
            return result_df.sort_values('similarity', ascending=False)
            
        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            return pd.DataFrame()

    def substructure_search(self, df: pd.DataFrame,
                           query_smarts: str,
                           smiles_column: str) -> pd.DataFrame:
        """
        Search compounds containing a specific substructure using SMARTS pattern
        """
        try:
            pattern = Chem.MolFromSmarts(query_smarts)
            if not pattern:
                return pd.DataFrame()

            def has_substructure(smiles: str) -> bool:
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    return bool(mol and mol.HasSubstructMatch(pattern))
                except:
                    return False

            result_df = df.copy()
            mask = result_df[smiles_column].apply(has_substructure)
            return result_df[mask]

        except Exception as e:
            print(f"Error in substructure search: {str(e)}")
            return pd.DataFrame()
