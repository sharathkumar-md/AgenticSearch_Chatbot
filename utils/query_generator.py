import re
import pandas as pd
from langchain.prompts import PromptTemplate
from typing import List, Optional

class QueryGenerator:
    @staticmethod
    def extract_placeholders(prompt: str) -> List[str]:
        """Extract placeholders from a given prompt using regex."""
        return re.findall(r"{(.*?)}", prompt)

    @staticmethod
    def generate_queries(query: str, df: pd.DataFrame) -> List[str]:
        """
        Generate dynamic queries based on a template and DataFrame.

        Args:
            query: Query template with placeholders
            df: DataFrame containing data for placeholders

        Returns:
            List[str]: List of formatted queries
        """
        placeholders = QueryGenerator.extract_placeholders(query)
        
        if not placeholders:
            return [query]

        try:
            allowed_columns = df.columns.tolist()
            missing_columns = [col for col in placeholders if col not in allowed_columns]

            if missing_columns:
                raise ValueError(f"Missing columns in DataFrame: {missing_columns}")

            prompt_template = PromptTemplate(input_variables=placeholders, template=query)
            
            formatted_queries = []
            for _, row in df.iterrows():
                try:
                    formatted_query = prompt_template.format(**row.to_dict())
                    formatted_queries.append(formatted_query)
                except KeyError as e:
                    print(f"Error: Missing data for placeholder {e} in row {row.to_dict()}")
                except Exception as e:
                    print(f"Unexpected error formatting query for row {row.to_dict()}: {e}")

            return formatted_queries

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []