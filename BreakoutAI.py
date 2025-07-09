import streamlit as st
from streamlit_gsheets import GSheetsConnection
from io import StringIO
import pandas as pd
import os
from pathlib import Path
from main import WebSearchPipeline
from config.settings import GROQ_MODEL_LIST, GOOGLE_MODEL_LIST
from agents.tools import SearchTools

def initialize_session_state():
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'data_source_type' not in st.session_state:
        st.session_state.data_source_type = None

def handle_file_upload():
    if st.session_state.uploaded_file is not None:
        df = pd.read_csv(st.session_state.uploaded_file)
        st.session_state.df = df
        st.session_state.data_source_type = 'csv'
        st.success("CSV uploaded successfully!")

def handle_gsheet_connection(sheet_url):
    if sheet_url.startswith("https://"):
        try:
            os.makedirs(".streamlit", exist_ok=True)
            with open(".streamlit/secrets.toml", "w") as f:
                f.write(f'[connections.gsheets]\nspreadsheet = "{sheet_url}"')
            
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read()
            st.session_state.df = df
            st.session_state.data_source_type = 'gsheet'
            st.success("Google Sheet connected successfully!")
        except Exception as e:
            st.error(f"Error connecting to Google Sheets: {e}")

def main():
    st.title("Web Search Pipeline")
    initialize_session_state()

    # Sidebar Configuration
    st.sidebar.title("Pipeline Settings")

    # Data Source Section in Sidebar
    st.sidebar.subheader("Data Source")
    data_source_option = st.sidebar.radio(
        "Choose data source",
        ["Upload CSV", "Connect Google Sheet"],
        key="data_source_radio"
    )

    if data_source_option == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Upload a CSV file",
            type=["csv"],
            key="uploaded_file",
            on_change=handle_file_upload
        )
    else:
        sheet_url = st.sidebar.text_input("Enter Google Sheet link:")
        if sheet_url:
            handle_gsheet_connection(sheet_url)

    # Reset Data Button
    if st.sidebar.button("Reset Data"):
        st.session_state.df = None
        st.session_state.results_df = None
        st.session_state.results = None
        st.session_state.data_source_type = None
        st.experimental_rerun()

    # Rest of the Sidebar Configuration
    show_df = st.sidebar.checkbox("Show DataFrame", value=True)
    no_row_to_show = st.sidebar.number_input("Number of rows to display", min_value=1, step=1, value=5)
    
    model_source = st.sidebar.selectbox("Select Model Source", ["groq", "google"])
    model_list = GROQ_MODEL_LIST if model_source == "groq" else GOOGLE_MODEL_LIST
    selected_model = st.sidebar.selectbox("Select Model", model_list)

    num_rows = st.sidebar.number_input("Number of rows to process", min_value=1, step=1, value=1)

    # Tools Selection
    st.sidebar.subheader("Available Tools")
    tools = SearchTools.get_tool_list()
    tool_names = [tool.name for tool in tools]
    selected_tool = st.sidebar.selectbox("Select Tools to Use", tool_names)

    tool_index = next((i for i, tool in enumerate(tools) if tool.name == selected_tool), 0)

    # Main Content Area
    if st.session_state.df is not None:
        if show_df:
            st.subheader("Loaded DataFrame")
            st.dataframe(st.session_state.df.head(no_row_to_show))

        # Query input
        st.subheader("Search Query")
        query_template = st.text_input(
            "Enter your query template:",
            "Get me the details of the {Company_Name}"
        )

        # Process Button
        if st.button("Start Processing"):
            with st.spinner("Processing... Please wait."):
                try:
                    pipeline = WebSearchPipeline(
                        data_source=st.session_state.df,
                        query_template=query_template,
                        model_name=selected_model,
                        output_path="search_results.csv",
                        rate_limit=1.0,
                        num_rows=num_rows,
                        tools=[tools[tool_index]],
                    )
                    results_df, results = pipeline.run()
                    
                    # Store results in session state
                    st.session_state.results_df = results_df
                    st.session_state.results = results

                except Exception as e:
                    st.error(f"Error during processing: {e}")

        # Display Results (if they exist in session state)
        if st.session_state.results_df is not None:
            st.subheader("Search Results")
            st.dataframe(st.session_state.results_df)

            st.subheader("Results")
            st.write(st.session_state.results)

            # Download Button
            st.subheader("Output File")
            st.download_button(
                label="Download results",
                data=st.session_state.results_df.to_csv(index=False),
                file_name="search_results.csv",
                mime="text/csv",
            )
    else:
        st.info("Please upload a CSV file or connect a Google Sheet to begin.")

if __name__ == "__main__":
    main()