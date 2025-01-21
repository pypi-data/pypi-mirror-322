#!/usr/bin/env python3
"""
DataBuster - Command Line Interface
=================================

A command-line interface for analyzing chemical compounds with support for:
- Structure analysis and molecular descriptors
- Duplicate detection and salt analysis
- Chirality analysis and stereochemistry
- Advanced compound type detection (peptide-like, macrocyclic, sugar-like)
- Drug-likeness assessment

Usage Examples
-------------
1. Basic analysis with all features:
   python databuster.py analyze input.csv --smiles-column "SMILES"

2. Specific analysis types using short aliases:
   python databuster.py analyze input.csv --smiles-column "SMILES" --analysis-types d m
   (d: duplicates, m: molecular descriptors)

3. Export results to custom location:
   python databuster.py analyze input.csv --smiles-column "SMILES" --output results.csv

4. Run all available analyses:
   python databuster.py analyze input.csv --smiles-column "SMILES" --analysis-types all
"""

import argparse
import sys
import pandas as pd
from utils.chemical_analysis import ChemicalAnalyzer
from typing import List, Dict
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Analysis type mappings
ANALYSIS_TYPE_ALIASES = {
    'd': 'Duplicate Detection',
    'c': 'Chirality Analysis',
    's': 'Salt Detection',
    'm': 'Molecular Descriptors',
    'o': 'Others'
}


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser with detailed help messages."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze',
                                           help='Analyze chemical compounds')
    analyze_parser.add_argument('input_file',
                                type=str,
                                help='Input CSV file containing compound data')
    analyze_parser.add_argument(
        '--smiles-column',
        type=str,
        required=True,
        help='Name of the column containing SMILES strings')

    # Analysis types with aliases
    analysis_help = """
    Types of analysis to perform. Use aliases for shorter commands:
    - d: Duplicate Detection
    - c: Chirality Analysis
    - s: Salt Detection
    - m: Molecular Descriptors
    - o: Others (peptide-like, macrocyclic, sugar-like)
    - all: Run all analysis types
    """
    analyze_parser.add_argument('--analysis-types',
                                nargs='+',
                                default=['all'],
                                help=analysis_help)
    analyze_parser.add_argument(
        '--output',
        type=str,
        default='analysis_results.csv',
        help=
        'Output file path for analysis results (default: analysis_results.csv)'
    )
    analyze_parser.add_argument('--log-level',
                                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                                default='INFO',
                                help='Set the logging level (default: INFO)')

    return parser


def validate_input_file(file_path: str) -> bool:
    """Validate input file exists and is readable."""
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Input file not found: {file_path}")
            return False
        if not path.suffix.lower() == '.csv':
            logger.error(f"Input file must be a CSV file: {file_path}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error validating input file: {str(e)}")
        return False


def process_analysis(df: pd.DataFrame, analysis_types: List[str],
                     smiles_column: str) -> Dict:
    """Process compounds with complete analysis workflow"""
    results = {}
    try:
        if 'all' in analysis_types:
            analysis_types = list(ANALYSIS_TYPE_ALIASES.values())
        else:
            # Convert aliases to full names
            analysis_types = [
                ANALYSIS_TYPE_ALIASES.get(t, t) for t in analysis_types
            ]

        smiles_list = df[smiles_column].tolist()
        if not smiles_list:
            raise ValueError("No SMILES data found")

        # Initialize complete analysis DataFrame
        complete_df = df.copy()
        complete_df['Valid_SMILES'] = [
            ChemicalAnalyzer.validate_smiles(s) for s in smiles_list
        ]

        # Process each analysis type
        for analysis_type in analysis_types:
            logger.info(f"Processing {analysis_type}...")

            if analysis_type == "Molecular Descriptors":
                descriptors = []
                for smiles in smiles_list:
                    desc = ChemicalAnalyzer.calculate_descriptors(smiles)
                    if desc:
                        desc["SMILES"] = smiles
                        descriptors.append(desc)
                if descriptors:
                    desc_df = pd.DataFrame(descriptors)
                    results["Molecular Descriptors"] = desc_df
                    # Merge descriptor results with complete_df
                    complete_df = complete_df.merge(desc_df,
                                                    on="SMILES",
                                                    how="left")

            elif analysis_type == "Duplicate Detection":
                duplicates = ChemicalAnalyzer.identify_duplicates(smiles_list)
                if duplicates:
                    results["Duplicate Detection"] = duplicates
                    # Add duplicate information to complete_df
                    complete_df['Has_Exact_Duplicates'] = False
                    complete_df['Has_Desalted_Duplicates'] = False
                    complete_df['Has_Similar_Duplicates'] = False
                    complete_df['Exact_Duplicate_Group'] = None
                    complete_df['Desalted_Duplicate_Group'] = None
                    complete_df['Similar_Duplicate_Group'] = None
                    complete_df['Exact_Group_Size'] = 0
                    complete_df['Desalted_Group_Size'] = 0
                    complete_df['Similar_Group_Size'] = 0

                    for dup_type in ['exact', 'desalted', 'similar']:
                        if dup_type in duplicates:
                            for group_id, indices in duplicates[
                                    dup_type].items():
                                group_size = len(indices)
                                for idx in indices:
                                    smiles = df.iloc[idx][smiles_column]
                                    complete_df.loc[
                                        complete_df[smiles_column] == smiles,
                                        f'Has_{dup_type.capitalize()}_Duplicates'] = True
                                    complete_df.loc[
                                        complete_df[smiles_column] == smiles,
                                        f'{dup_type.capitalize()}_Duplicate_Group'] = f"group_{group_id}"
                                    complete_df.loc[
                                        complete_df[smiles_column] == smiles,
                                        f'{dup_type.capitalize()}_Group_Size'] = group_size

            elif analysis_type == "Chirality Analysis":
                chiral_results = []
                for smiles in smiles_list:
                    is_chiral, center_count = ChemicalAnalyzer.detect_chirality(
                        smiles)
                    chiral_results.append({
                        'SMILES': smiles,
                        'Is_Chiral': is_chiral,
                        'Chiral_Centers': center_count
                    })
                chiral_df = pd.DataFrame(chiral_results)
                results["Chirality Analysis"] = chiral_df
                complete_df = complete_df.merge(chiral_df,
                                                on="SMILES",
                                                how="left")

            elif analysis_type == "Salt Detection":
                salt_results = []
                for smiles in smiles_list:
                    has_salt = ChemicalAnalyzer.identify_salts(smiles)
                    salt_results.append({
                        'SMILES': smiles,
                        'Has_Salt': has_salt
                    })
                salt_df = pd.DataFrame(salt_results)
                results["Salt Detection"] = salt_df
                complete_df = complete_df.merge(salt_df,
                                                on="SMILES",
                                                how="left")

            elif analysis_type == "Others":
                other_results = []
                for smiles in smiles_list:
                    other_results.append({
                        'SMILES':
                        smiles,
                        'Is_Peptide_Like':
                        ChemicalAnalyzer.is_peptide_like(smiles),
                        'Is_Macrocyclic':
                        ChemicalAnalyzer.is_macrocyclic(smiles),
                        'Is_Sugar_Like':
                        ChemicalAnalyzer.is_sugar_like(smiles),
                        'Is_Drug_Like':
                        ChemicalAnalyzer.is_drug_like(smiles)
                    })
                other_df = pd.DataFrame(other_results)
                results["Others"] = other_df
                complete_df = complete_df.merge(other_df,
                                                on="SMILES",
                                                how="left")

        results['complete_analysis'] = complete_df
        return results

    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise


def run_analysis(args: argparse.Namespace) -> int:
    """Run chemical compound analysis based on command line arguments."""
    try:
        # Validate input file
        if not validate_input_file(args.input_file):
            return 1

        # Read input data
        logger.info(f"Reading input file: {args.input_file}")
        df = pd.read_csv(args.input_file)

        if args.smiles_column not in df.columns:
            logger.error(
                f"SMILES column '{args.smiles_column}' not found in input file"
            )
            return 1

        # Process analysis
        logger.info("Starting analysis...")
        results = process_analysis(df, args.analysis_types, args.smiles_column)

        # Save results
        if results:
            output_path = args.output
            logger.info(f"Saving results to {output_path}")

            # Save complete analysis to CSV
            complete_df = results['complete_analysis']
            complete_df.to_csv(output_path, index=False)
            logger.info(f"Complete analysis saved to {output_path}")

            # Save detailed results as JSON
            json_output = output_path.replace('.csv', '.json')
            with open(json_output, 'w') as f:
                # Convert non-serializable objects to strings if needed
                serializable_results = {
                    k: (v.to_dict('records')
                        if isinstance(v, pd.DataFrame) else v)
                    for k, v in results.items() if k !=
                    'complete_analysis'  # Exclude complete_analysis from JSON
                }
                json.dump(serializable_results, f, indent=2)
            logger.info(f"Detailed analysis results saved to {json_output}")

            return 0
        else:
            logger.error("No results generated")
            return 1

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return 1


def main():
    """Main entry point for the CLI."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    if args.command == 'analyze':
        sys.exit(run_analysis(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
