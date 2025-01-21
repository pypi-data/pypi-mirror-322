from rdkit import Chem
from rdkit.Chem import AllChem
from typing import List, Dict, Tuple

class StructureFilters:
    @staticmethod
    def detect_peptide_like(smiles: str) -> Tuple[bool, str]:
        """
        Detect peptide-like molecules based on:
        1. Presence of peptide bonds
        2. Number of amino acid residues
        3. Linear peptide structure
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False, "Invalid SMILES"

            # SMARTS pattern for peptide bond
            peptide_bond = Chem.MolFromSmarts('[NX3,NX4+][CX4H1,CX4H2][CX3](=[OX1])[NX3,NX4+][CX4H1,CX4H2][CX3](=[OX1])')
            
            # SMARTS patterns for common amino acid side chains
            aa_patterns = {
                'Ala': '[CH3][CH]([NH2])[C](=O)[OH]',
                'Gly': '[NH2][CH2][C](=O)[OH]',
                'Val': '[CH3][CH]([CH3])[CH]([NH2])[C](=O)[OH]',
                'Leu': '[CH3][CH]([CH3])[CH2][CH]([NH2])[C](=O)[OH]',
                'Ile': '[CH3][CH2][CH]([CH3])[CH]([NH2])[C](=O)[OH]',
                'Pro': '[NH][CH2][CH2][CH2][CH]([C](=O)[OH])',
                'Phe': '[c]1[c][c][c]([CH2][CH]([NH2])[C](=O)[OH])[c][c]1',
                'Trp': '[c]1[c][n][c]2[c]([CH2][CH]([NH2])[C](=O)[OH])[c][c][c][c]12',
                'Ser': '[OH][CH2][CH]([NH2])[C](=O)[OH]',
                'Thr': '[CH3][CH]([OH])[CH]([NH2])[C](=O)[OH]',
                'Cys': '[SH][CH2][CH]([NH2])[C](=O)[OH]',
                'Met': '[CH3][S][CH2][CH2][CH]([NH2])[C](=O)[OH]',
                'Asn': '[NH2][C](=O)[CH2][CH]([NH2])[C](=O)[OH]',
                'Gln': '[NH2][C](=O)[CH2][CH2][CH]([NH2])[C](=O)[OH]',
                'Asp': '[OH][C](=O)[CH2][CH]([NH2])[C](=O)[OH]',
                'Glu': '[OH][C](=O)[CH2][CH2][CH]([NH2])[C](=O)[OH]',
                'Lys': '[NH2][CH2][CH2][CH2][CH2][CH]([NH2])[C](=O)[OH]',
                'Arg': '[NH2][C](=[NH])[NH][CH2][CH2][CH2][CH]([NH2])[C](=O)[OH]',
                'His': '[c]1[n][c][n][c]([CH2][CH]([NH2])[C](=O)[OH])[c]1'
            }

            # Check for peptide bonds
            peptide_matches = mol.GetSubstructMatches(peptide_bond)
            if not peptide_matches:
                return False, "No peptide bonds found"

            # Count amino acid residues
            aa_count = 0
            found_aa = []
            for aa_name, pattern in aa_patterns.items():
                aa_pattern = Chem.MolFromSmarts(pattern)
                if mol.HasSubstructMatch(aa_pattern):
                    aa_count += 1
                    found_aa.append(aa_name)

            # Define criteria for peptide-like molecules
            min_peptide_bonds = 1
            min_aa_residues = 2

            is_peptide = (
                len(peptide_matches) >= min_peptide_bonds and
                aa_count >= min_aa_residues
            )

            if is_peptide:
                details = f"Found {len(peptide_matches)} peptide bonds and {aa_count} amino acid residues ({', '.join(found_aa)})"
                return True, details
            else:
                return False, f"Insufficient peptide characteristics (bonds: {len(peptide_matches)}, residues: {aa_count})"

        except Exception as e:
            return False, f"Error in peptide detection: {str(e)}"

    @staticmethod
    def detect_macrocycle(smiles: str) -> Tuple[bool, str]:
        """
        Detect macrocyclic structures based on:
        1. Ring size (typically ≥ 12 atoms)
        2. Ring composition
        3. Optional: presence of specific functional groups
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if not mol:
                return False, "Invalid SMILES"

            # Detect cycles
            ring_info = mol.GetRingInfo()
            if not ring_info.NumRings():
                return False, "No rings found"

            # Get ring sizes
            ring_sizes = []
            for ring in ring_info.AtomRings():
                ring_sizes.append(len(ring))

            # Define macrocycle criteria
            min_ring_size = 12  # Common definition for macrocycles
            max_ring_size = 60  # Upper limit for typical macrocycles

            # Check for macrocycles
            macro_rings = [size for size in ring_sizes if min_ring_size <= size <= max_ring_size]
            
            if not macro_rings:
                return False, f"No macrocycles found (ring sizes: {ring_sizes})"

            # Additional analysis for found macrocycles
            details = []
            for ring_size in macro_rings:
                # Basic classification
                if ring_size < 14:
                    category = "small macrocycle"
                elif ring_size < 20:
                    category = "medium macrocycle"
                else:
                    category = "large macrocycle"
                
                details.append(f"{ring_size}-membered ring ({category})")

            # Check for specific functional groups within macrocycles
            functional_groups = {
                'ester': '[#6][CX3](=O)[OX2H0][#6]',
                'amide': '[NX3][CX3](=[OX1])[#6]',
                'ether': '[OD2]([#6])[#6]',
                'sulfide': '[#16X2H0][#6]'
            }

            found_groups = []
            for group_name, smarts in functional_groups.items():
                pattern = Chem.MolFromSmarts(smarts)
                if mol.HasSubstructMatch(pattern):
                    found_groups.append(group_name)

            return True, f"Found {len(macro_rings)} macrocycle(s): {', '.join(details)}. " + \
                       (f"Functional groups: {', '.join(found_groups)}" if found_groups else "No specific functional groups found")

        except Exception as e:
            return False, f"Error in macrocycle detection: {str(e)}"

# Example usage:
if __name__ == "__main__":
    # Example SMILES strings
    peptide_smiles = "CC(=O)N[C@@H](C)C(=O)N[C@@H](Cc1ccccc1)C(=O)O"  # Simple tripeptide
    macrocycle_smiles = "O=C1CCCCCCCCCCC(=O)NCCCCN1"  # Simple macrocyclic structure

    # Test peptide detection
    is_peptide, peptide_details = StructureFilters.detect_peptide_like(peptide_smiles)
    print(f"\nPeptide Analysis:")
    print(f"Is peptide-like? {is_peptide}")
    print(f"Details: {peptide_details}")

    # Test macrocycle detection
    is_macro, macro_details = StructureFilters.detect_macrocycle(macrocycle_smiles)
    print(f"\nMacrocycle Analysis:")
    print(f"Is macrocyclic? {is_macro}")
    print(f"Details: {macro_details}")