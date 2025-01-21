# DataBuster

A sophisticated chemical compound analysis platform for drug discovery research and molecular data pre=processing through advanced computational chemistry tools.

## Developed By

Suneel Kumar BVS, Ph.D.  
ATOMICAS AI SOLUTIONS PRIVATE LIMITED  
Website: https://theatomicas.io  
Contact: suneel@theatomicas.io, suneelkumar.bvs@gmail.com

## Official Repo
https://github.com/suneelbvs/databuster

## Overview

DataBuster is a powerful platform designed to deep-dive into the datasets and to provide comprehensive analysis of chemical datasets. It provides advanced cheminformatics capabilities to provide an intuitive and powerful analysis which ultimately helps the users to understand the dataset better, to preprocess the dataset for modelling.

## Features

- Structure analysis
- Molecular descriptors calculation
- Duplicate detection
- Chirality analysis
- Salt detection
- Structure standardization
- Batch processing
- Command-line interface

## Installation

```bash
pip install databuster
```

## Usage

### Command Line Interface (CLI)

The tool provides a powerful command-line interface for batch processing and automation.

#### Basic Usage

Usage Examples
-------------
```bash
1. Basic analysis with all features:
   python databuster.py analyze input.csv --smiles-column "SMILES"

2. Specific analysis types using short aliases:
   python databuster.py analyze input.csv --smiles-column "SMILES" --analysis-types d m
   (d: duplicates, m: molecular descriptors)

3. Export results to custom location:
   python databuster.py analyze input.csv --smiles-column "SMILES" --output results.csv

4. Run all available analyses:
   python databuster.py analyze input.csv --smiles-column "SMILES" --analysis-types all
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Developments, and Feedback

Write to suneel@theatomicas.io for any feedback, ideas to implement, and collaborate.

## Citation

In progress, will update the details by Jan 15, 2025