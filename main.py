import pandas as pd
from typing import Optional, List
import time
from data.data_loader import DataLoader
from models.llm import LLMFactory
from agents.tools import SearchTools
from agents.search_agent import SearchAgent
from utils.query_generator import QueryGenerator
from utils.result_handler import ResultHandler


class WebSearchPipeline:
    def __init__(
        self,
        data_source: pd.DataFrame,
        query_template: str,
        model_name: str,
        tools: List,  # Parameterized tools list
        output_path: Optional[str] = None,
        rate_limit: float = 1.0,  # Time in seconds between requests
        num_rows: Optional[int] = None,
    ):
        self.data_source = data_source
        self.query_template = query_template
        self.model_name = model_name
        self.output_path = output_path or "search_results.csv"
        self.rate_limit = rate_limit
        self.num_rows = num_rows
        self.tools = tools  # Assign tools to an instance variable

        # Initialize components
        self.df = self._load_data()
        self.llm = LLMFactory.create_llm(model_name)
        self.agent = SearchAgent(self.llm, self.tools)

    def _load_data(self) -> pd.DataFrame:
        """Load and validate input data."""
        df = self.data_source

        # Validate that all placeholders in template have corresponding columns
        placeholders = QueryGenerator.extract_placeholders(self.query_template)
        DataLoader.validate_columns(df, placeholders)

        if self.num_rows is not None:
            df = df.head(self.num_rows)

        return df

    def run(self, save_intermediate: bool = True) -> pd.DataFrame:
        """
        Execute the web search pipeline.

        Args:
            save_intermediate: Whether to save intermediate results

        Returns:
            pd.DataFrame: Results DataFrame
        """
        print(f"Starting web search for {len(self.df)} rows...")

        # Generate queries for each row
        queries = QueryGenerator.generate_queries(self.query_template, self.df)
        results = []

        # Execute searches with progress tracking
        for i, query in enumerate(queries, 1):
            try:
                print(f"Processing row {i}/{len(queries)}: {query}")
                result = self.agent.search(query)
                results.append(result)

                # Save intermediate results
                if save_intermediate and i % 5 == 0:  # Save every 5 rows
                    intermediate_df = ResultHandler.create_results_dataframe(
                        self.df.iloc[:i],
                        queries[:i],
                        results
                    )
                    intermediate_path = f"intermediate_results_{i}.csv"
                    ResultHandler.save_results(intermediate_df, intermediate_path)
                    print(f"Saved intermediate results to {intermediate_path}")

                # Rate limiting
                if i < len(queries):  # Don't wait after the last query
                    time.sleep(self.rate_limit)

            except Exception as e:
                print(f"Error processing row {i}: {e}")
                results.append({"output": f"Error: {str(e)}"})

        # Create final results DataFrame
        result_df = ResultHandler.create_results_dataframe(
            self.df,
            queries,
            results
        )

        # Save final results
        ResultHandler.save_results(result_df, self.output_path)
        print(f"Search completed. Results saved to {self.output_path}")

        return result_df,results
