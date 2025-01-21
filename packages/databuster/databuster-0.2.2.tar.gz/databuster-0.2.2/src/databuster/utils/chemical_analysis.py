from typing import Dict, List
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors, DataStructs
from typing import Dict, List, Optional, Tuple

import requests
import hashlib
from typing import Optional
import logging


class ChemicalAnalyzer:
    PUBCHEM_API_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    @staticmethod
    def get_structure_from_pubchem(smiles: str,
                                   size: int = 300) -> Optional[str]:
        """
        Get 2D structure image URL from PubChem using SMILES

        Args:
            smiles: SMILES string of the molecule
            size: Image size in pixels

        Returns:
            URL to the structure image or None if not found
        """
        try:
            # Create a unique cache key for this SMILES
            cache_key = hashlib.md5(smiles.encode()).hexdigest()

            # First try to get compound info using SMILES
            smiles_url = f"{ChemicalAnalyzer.PUBCHEM_API_BASE}/compound/smiles/{smiles}/PNG"
            params = {
                'record_type': '2d',
                'image_size': f"{size}x{size}",
                'cache': cache_key
            }

            response = requests.get(smiles_url, params=params)

            if response.status_code == 200:
                return response.url
            else:
                logging.warning(
                    f"Failed to get structure from PubChem for SMILES {smiles}"
                )
                return None

        except Exception as e:
            logging.error(f"Error fetching structure from PubChem: {str(e)}")
            return None

    @staticmethod
    def validate_smiles(smiles: str) -> bool:
        """Validate SMILES string"""
        if not isinstance(smiles, str):
            logging.warning(f"Invalid SMILES input type: {type(smiles)}")
            return False
        try:
            mol = Chem.MolFromSmiles(smiles)
            return mol is not None
        except Exception as e:
            logging.error(f"SMILES validation error: {str(e)}")
            return False

    @staticmethod
    def calculate_descriptors(smiles: str) -> Dict[str, float]:
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                # Basic Lipinski descriptors
                mw = Descriptors.ExactMolWt(mol)
                logp = Descriptors.MolLogP(mol)
                hbd = Descriptors.NumHDonors(mol)
                hba = Descriptors.NumHAcceptors(mol)
                psa = Descriptors.TPSA(mol)
                rotatable = Descriptors.NumRotatableBonds(mol)

                # Count Lipinski violations
                violations = 0
                if mw > 500: violations += 1
                if logp > 5: violations += 1
                if hbd > 5: violations += 1
                if hba > 10: violations += 1

                return {
                    'MW': mw,
                    'LogP': logp,
                    'HBD': hbd,
                    'HBA': hba,
                    'TPSA': psa,
                    'RotBonds': rotatable,
                    'Lipinski_Violations': violations,
                    'Rings': Descriptors.RingCount(mol),
                    'Aromatic_Rings': Descriptors.NumAromaticRings(mol),
                    'Fsp3': Descriptors.FractionCSP3(mol)
                }
            return {}
        except Exception as e:
            print(f"Error calculating descriptors: {str(e)}")
            return {}

    @staticmethod
    def identify_duplicates(
            smiles_list: List[str]) -> Dict[str, Dict[str, List[int]]]:
        """
        Identifies duplicate chemical structures in a list of SMILES strings.
        Includes salt-removed duplicates and similar structures (carboxylic acid/carboxylate pairs).

        Args:
            smiles_list (List[str]): List of SMILES strings representing chemical structures.

        Returns:
            Dict[str, Dict[str, List[int]]]: Dictionary containing different types of duplicates:
                - 'exact': Exact structure matches
                - 'desalted': Matches after salt removal
                - 'similar': Structurally similar compounds (carboxylic acid/carboxylate pairs)
        """
        duplicates = {'exact': {}, 'desalted': {}, 'similar': {}}

        # Process exact duplicates
        inchi_dict = {}
        desalted_dict = {}
        similar_dict = {}

        for idx, smiles in enumerate(smiles_list):
            try:
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    # Exact duplicates
                    inchi_key = Chem.MolToInchiKey(mol)
                    if inchi_key in inchi_dict:
                        inchi_dict[inchi_key].append(idx)
                    else:
                        inchi_dict[inchi_key] = [idx]

                    # Desalted duplicates
                    fragments = Chem.GetMolFrags(mol, asMols=True)
                    if len(fragments) > 1:
                        # Get largest fragment as parent
                        parent_mol = max(fragments,
                                         key=lambda m: m.GetNumAtoms())
                        parent_inchi = Chem.MolToInchiKey(parent_mol)
                        if parent_inchi in desalted_dict:
                            desalted_dict[parent_inchi].append(idx)
                        else:
                            desalted_dict[parent_inchi] = [idx]

                    # Check for carboxylic acid/carboxylate pairs
                    acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
                    salt_pattern = Chem.MolFromSmarts('[CX3](=O)[O-]')

                    has_acid = mol.HasSubstructMatch(acid_pattern)
                    has_salt = mol.HasSubstructMatch(salt_pattern)

                    if has_acid or has_salt:
                        # Generate a canonical form ignoring acid/salt state
                        neutral_mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
                        Chem.RemoveHs(neutral_mol)
                        neutral_smiles = Chem.MolToSmiles(neutral_mol,
                                                          canonical=True)

                        if neutral_smiles in similar_dict:
                            similar_dict[neutral_smiles].append(idx)
                        else:
                            similar_dict[neutral_smiles] = [idx]

                else:
                    logging.warning(f"Invalid SMILES at index {idx}: {smiles}")
            except Exception as e:
                logging.error(
                    f"Error processing SMILES at index {idx}: {smiles}. Error: {str(e)}"
                )
                continue

        # Filter and organize results
        duplicates['exact'] = {
            k: v
            for k, v in inchi_dict.items() if len(v) > 1
        }
        duplicates['desalted'] = {
            k: v
            for k, v in desalted_dict.items() if len(v) > 1
        }
        duplicates['similar'] = {
            k: v
            for k, v in similar_dict.items() if len(v) > 1
        }

        return duplicates

    @staticmethod
    def detect_chirality(smiles: str) -> Tuple[bool, int]:
        """Detect chiral centers and return count"""
        if not ChemicalAnalyzer.validate_smiles(smiles):
            return False, 0

        try:
            mol = Chem.MolFromSmiles(smiles)
            chiral_centers = Chem.FindMolChiralCenters(mol,
                                                       includeUnassigned=True)
            return bool(chiral_centers), len(chiral_centers)
        except Exception as e:
            logging.error(f"Error detecting chirality: {str(e)}")
            return False, 0

    @staticmethod
    def process_chirality_info(complete_df, smiles_column):
        """
        Add chiral information to the DataFrame including:
        1. Compounds with stereo centers
        2. Identifying chiral pairs with different stereochemistry
        """
        logger = logging.getLogger(__name__)
        logger.info("Starting chirality processing")

        # Initialize chiral information columns
        complete_df['Is_Chiral'] = False
        complete_df['Chiral_Group'] = "None"
        complete_df['Group_Size'] = 0
        complete_df['Stereo'] = "None"
        complete_df['ChiralCenterCount'] = 0

        # Step 1: Detect chiral centers for each compound
        canonical_map = {}  # For identifying stereoisomer groups

        for idx, row in complete_df.iterrows():
            smiles = row[smiles_column]
            try:
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    # Find chiral centers
                    chiral_centers = Chem.FindMolChiralCenters(
                        mol, includeUnassigned=True)
                    chiral_count = len(chiral_centers)
                    complete_df.at[idx, 'ChiralCenterCount'] = chiral_count
                    if chiral_count > 0:
                        complete_df.at[idx, 'Is_Chiral'] = True

                        # Check for specified stereochemistry
                        has_specified_stereo = any(
                            center[1] != '?' for center in chiral_centers)
                        complete_df.at[
                            idx,
                            'Stereo'] = 'Yes' if has_specified_stereo else 'No'

                        # Add canonical structure without stereochemistry
                        mol_no_stereo = Chem.MolFromSmiles(
                            Chem.MolToSmiles(mol, isomericSmiles=False))
                        canonical_smiles = Chem.MolToSmiles(mol_no_stereo,
                                                            canonical=True)
                        if canonical_smiles not in canonical_map:
                            canonical_map[canonical_smiles] = []
                        canonical_map[canonical_smiles].append((idx, smiles))
            except Exception as e:
                logger.error(
                    f"Error processing SMILES at index {idx}: {str(e)}")

        # Step 2: Group chiral compounds with different stereochemistry
        group_counter = 1
        for canonical_smiles, compounds in canonical_map.items():
            if len(compounds
                   ) > 1:  # Only consider groups with multiple stereoisomers
                unique_stereo = {}  # To store unique stereoisomers
                for idx, smiles in compounds:
                    mol = Chem.MolFromSmiles(smiles)
                    if mol:
                        stereo_smiles = Chem.MolToSmiles(mol,
                                                         isomericSmiles=True)
                        unique_stereo[stereo_smiles] = idx

                if len(unique_stereo
                       ) > 1:  # Assign group if multiple stereoisomers
                    group_key = f"group_{group_counter}"
                    indices = list(unique_stereo.values())
                    for i in indices:
                        complete_df.at[i, 'Chiral_Group'] = group_key
                        complete_df.at[i, 'Group_Size'] = len(indices)
                    logger.info(
                        f"Assigned {group_key} to {len(indices)} compounds")
                    group_counter += 1

        logger.info("Completed chirality processing")
        logger.info(f"Processed {group_counter-1} chiral groups")
        return complete_df

    @staticmethod
    def identify_salts(smiles: str) -> bool:
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                fragments = Chem.GetMolFrags(mol, asMols=True)
                return len(fragments) > 1
            return False
        except Exception as e:
            print(f"Error identifying salts: {str(e)}")
            return False

    @staticmethod
    def standardize_compound(smiles: str) -> str:
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                return Chem.MolToSmiles(mol, canonical=True)
            return smiles
        except Exception as e:
            print(f"Error standardizing compound: {str(e)}")
            return smiles

    """ChemicalAnalyzer class methods for detecting compound types"""

    @staticmethod
    def is_peptide_like(smiles: str) -> bool:
        """Check if a compound is peptide-like"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False

            # Peptide bond pattern
            peptide_bond = Chem.MolFromSmarts('[NX3,NX4+][CX4H1,CX4H2][CX3](=[OX1])[NX3,NX4+][CX4H1,CX4H2][CX3](=[OX1])')

            # Check for peptide bonds
            peptide_matches = mol.GetSubstructMatches(peptide_bond)
            if not peptide_matches:
                return False

            # Count amino acid residues (simplified check)
            aa_pattern = Chem.MolFromSmarts('[NX3,NX4+][CX4H1,CX4H2][CX3](=[OX1])[OH,OX2H0]')
            aa_matches = mol.GetSubstructMatches(aa_pattern)

            # Define criteria for peptide-like molecules
            min_peptide_bonds = 1
            min_aa_residues = 2

            return len(peptide_matches) >= min_peptide_bonds and len(aa_matches) >= min_aa_residues

        except Exception as e:
            logging.error(f"Error in peptide detection: {str(e)}")
            return False

    @staticmethod
    def is_macrocyclic(smiles: str) -> bool:
        """Check if a compound is macrocyclic"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False

            # Get ring information
            ring_info = mol.GetRingInfo()
            if not ring_info.NumRings():
                return False

            # Define macrocycle criteria
            min_ring_size = 12  # Common definition for macrocycles
            max_ring_size = 60  # Upper limit for typical macrocycles

            # Check ring sizes
            for ring in ring_info.AtomRings():
                ring_size = len(ring)
                if min_ring_size <= ring_size <= max_ring_size:
                    return True

            return False

        except Exception as e:
            logging.error(f"Error in macrocycle detection: {str(e)}")
            return False

    @staticmethod
    def is_sugar_like(smiles: str) -> bool:
        """Check if a compound has sugar-like characteristics"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False

            # Patterns for sugar-like structures
            pyranose = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1][CR1][OR1]1')  # 6-membered ring with oxygen
            furanose = Chem.MolFromSmarts('[CR1]1[CR1][CR1][CR1][OR1]1')  # 5-membered ring with oxygen

            # Multiple hydroxyl groups
            hydroxyl = Chem.MolFromSmarts('[OX2H]')

            # Check for sugar-like characteristics
            has_pyranose = mol.HasSubstructMatch(pyranose)
            has_furanose = mol.HasSubstructMatch(furanose)
            hydroxyl_count = len(mol.GetSubstructMatches(hydroxyl))

            # Criteria for sugar-like compounds
            min_hydroxyls = 3
            return (has_pyranose or has_furanose) and hydroxyl_count >= min_hydroxyls

        except Exception as e:
            logging.error(f"Error in sugar detection: {str(e)}")
            return False

    @staticmethod
    def is_drug_like(smiles: str) -> bool:
        """Check if a compound follows Lipinski's Rule of Five and other drug-likeness criteria"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False

            # Calculate properties
            mw = Descriptors.ExactMolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = Descriptors.NumHDonors(mol)
            hba = Descriptors.NumHAcceptors(mol)
            tpsa = Descriptors.TPSA(mol)
            rotatable = Descriptors.NumRotatableBonds(mol)

            # Lipinski's Rule of Five with some flexibility
            mw_ok = mw <= 500
            logp_ok = -0.4 <= logp <= 5.6
            hbd_ok = hbd <= 5
            hba_ok = hba <= 10

            # Additional drug-likeness criteria
            tpsa_ok = tpsa <= 140
            rotatable_ok = rotatable <= 10

            # Allow one violation of Lipinski's rules
            lipinski_violations = sum(not x for x in [mw_ok, logp_ok, hbd_ok, hba_ok])

            return lipinski_violations <= 1 and tpsa_ok and rotatable_ok

        except Exception as e:
            logging.error(f"Error in drug-likeness detection: {str(e)}")
            return False