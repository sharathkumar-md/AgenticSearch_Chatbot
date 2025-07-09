# Interactive CSV Chat with Web Search Pipeline

This project is an intelligent web search and data analysis pipeline built with Streamlit. It allows users to upload CSV files or connect Google Sheets, run customized searches across their data using various AI models, and interact with the results through a chat interface.

**Video walkthrough of this project:** https://drive.google.com/file/d/175EDThXr_33pV0LXefQ05OVoK49OJgZt/view?usp=sharing

## 🚀 Features

- **Multiple Data Source Support**
  - CSV file upload
  - Google Sheets integration
  - Real-time data preview

- **Advanced Model Selection**
  - GROQ Models support (including Gemma, LLaMA variants)
  - Google Models support (Gemini variants)
  - Adjustable temperature settings
 
- **Integrated Various Search Tools**
  - **Tavily Search Results**: Powered by `Tavily`.
  - **Google Search**: `SerpAPIWrapper`.
  - **DuckDuckGo**: `DuckDuckGoSearchAPIWrapper`.
  - **Wikipedia**: For reliable knowledge retrieval using `WikipediaAPIWrapper`.
  - **Google Serper API**: Additional search capability with `GoogleSerperAPIWrapper`.


- **Customizable Search Pipeline**
  - Template-based query generation
  - Configurable execution parameters
  - Rate limiting for API calls

- **Interactive Results**
  - Real-time search progress tracking
  - Dynamic results display
  - Chat interface for exploring results

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
2.Create and activate a virtual environment:
```bash
python -m venv venv
source venv\Scripts\activate
```
3.Install required packages:
```bash
pip install -r requirements.txt
```
4.Create a .env file or rename the .env-example in the project root directory:

And place the required api key as mentioned in .env-example

5.Running the Application

Start the Streamlit app:
```bash
streamlit run .\BreakoutAI.py
```
