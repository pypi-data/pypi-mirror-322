import pandas as pd
import numpy as np
from typing import List, Dict, Any, Callable
import gc
import logging
import traceback

class BatchProcessor:
    @staticmethod
    def process_in_batches(data: pd.DataFrame,
                          batch_size: int,
                          process_func: Callable,
                          column: str = None) -> Dict[str, Any]:
        """
        Process large datasets in batches with memory optimization
        
        Args:
            data: Input dataframe
            batch_size: Size of each batch
            process_func: Function to process each batch
            column: Column to batch by (if None, batch by index)
        """
        logging.info(f"Starting batch processing with batch size: {batch_size}")
        
        if column and column not in data.columns:
            raise ValueError(f"Column {column} not found in dataframe")
            
        total_size = len(data)
        results = {}
        errors = []
        
        # Calculate number of batches
        num_batches = (total_size + batch_size - 1) // batch_size
        logging.info(f"Processing {total_size} records in {num_batches} batches")
        
        # Process batches sequentially
        for i in range(0, total_size, batch_size):
            batch_idx = i // batch_size
            try:
                batch_df = data.iloc[i:i + batch_size].copy()
                batch_result = process_func(batch_df)
                
                # Merge results based on their type
                for key, value in batch_result.items():
                    if key not in results:
                        if isinstance(value, pd.DataFrame):
                            results[key] = value
                        elif isinstance(value, dict):
                            results[key] = {}
                        elif isinstance(value, list):
                            results[key] = []
                        else:
                            results[key] = type(value)()
                                
                    if isinstance(value, pd.DataFrame):
                        if key in results:
                            results[key] = pd.concat([results[key], value])
                    elif isinstance(value, dict):
                        results[key].update(value)
                    elif isinstance(value, list):
                        results[key].extend(value)
                
                # Force garbage collection after each batch
                gc.collect()
                
            except Exception as e:
                errors.append({
                    'batch': batch_idx,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                })
        
        # Add error information if any occurred
        if errors:
            results['processing_errors'] = errors
            
        return results

    @staticmethod
    def estimate_optimal_batch_size(df: pd.DataFrame, target_memory_mb: int = 50) -> int:
        """
        Estimate optimal batch size based on dataframe memory usage with more conservative limits
        """
        try:
            # Calculate approximate memory per row
            row_size = df.memory_usage(deep=True).sum() / len(df)
            
            # Calculate batch size based on target memory
            batch_size = int((target_memory_mb * 1024 * 1024) / row_size)
            
            # Apply reasonable limits
            min_batch = 10
            max_batch = 200
            
            return max(min_batch, min(max_batch, batch_size))
        except:
            # Return a conservative default if estimation fails
            return 50
