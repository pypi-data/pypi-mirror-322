import pandas as pd
from typing import Dict

class DataProcessor:
    @staticmethod
    def load_csv(file) -> pd.DataFrame:
        try:
            df = pd.read_csv(file)
            if df.empty:
                raise ValueError("CSV file is empty")
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")

    @staticmethod
    def get_predefined_datasets() -> Dict[str, str]:
        return {
            "BACE": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv",
            "HIV": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/HIV.csv",
            "Tox21": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv",
            "SIDER": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/sider.csv",
            "ClinTox": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/clintox.csv",
            "BBBP": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv",
            "Clearance": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Clearance.csv"
        }

    @staticmethod
    def load_predefined_dataset(dataset_name: str) -> pd.DataFrame:
        datasets = DataProcessor.get_predefined_datasets()
        if dataset_name not in datasets:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        try:
            # Direct download to memory using pandas
            df = pd.read_csv(datasets[dataset_name])
            if df.empty:
                raise ValueError("Downloaded dataset is empty")
            return df
        except Exception as e:
            raise ValueError(f"Error loading dataset: {str(e)}")

    @staticmethod
    def prepare_download_report(results: Dict) -> pd.DataFrame:
        report_data = []
        for analysis_type, data in results.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    report_data.append({
                        "Analysis Type": analysis_type,
                        "Compound": key,
                        "Details": str(value)
                    })
            elif isinstance(data, list):
                for item in data:
                    report_data.append({
                        "Analysis Type": analysis_type,
                        "Compound": str(item),
                        "Details": ""
                    })
        return pd.DataFrame(report_data)
