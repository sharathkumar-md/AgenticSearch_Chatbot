import pandas as pd
from typing import List, Dict, Any

class ResultHandler:
    @staticmethod
    def process_agent_response(response: Dict[str, Any]) -> str:
        """
        Extract the final answer from the agent's response.
        
        Args:
            response: Raw response from the agent
            
        Returns:
            str: Final answer extracted from the response
        """
        if isinstance(response, dict) and 'output' in response:
            return response['output']
        return str(response)
    
    @staticmethod
    def create_results_dataframe(
        original_df: pd.DataFrame,
        queries: List[str],
        results: List[Dict[str, Any]],
        result_column_name: str = "search_result"
    ) -> pd.DataFrame:
        """
        Create a DataFrame combining original data with search results.
        
        Args:
            original_df: Original input DataFrame
            queries: List of queries executed
            results: List of search results from the agent
            result_column_name: Name for the column containing search results
            
        Returns:
            pd.DataFrame: Combined DataFrame with original data and results
        """
        # Create a copy of the original DataFrame
        result_df = original_df.copy()
        
        # Add columns for queries and results
        result_df['generated_query'] = queries
        result_df[result_column_name] = [
            ResultHandler.process_agent_response(result) 
            for result in results
        ]
        
        return result_df
    
    @staticmethod
    def save_results(
        df: pd.DataFrame,
        output_path: str,
        format: str = 'csv'
    ) -> None:
        """
        Save the results DataFrame to a file.
        
        Args:
            df: DataFrame to save
            output_path: Path where to save the file
            format: Output format ('csv' or 'excel')
        """
        if format.lower() == 'csv':
            df.to_csv(output_path, index=False)
        elif format.lower() == 'excel':
            df.to_excel(output_path, index=False)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'excel'")