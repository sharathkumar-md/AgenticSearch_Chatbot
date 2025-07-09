from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os
from pathlib import Path
import json
from main import WebSearchPipeline
from config.settings import GROQ_MODEL_LIST, GOOGLE_MODEL_LIST
from agents.tools import SearchTools
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Configure COR
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class SearchRequest(BaseModel):
    query_template: str
    model_source: str
    model_name: str
    tool_name: str
    num_rows: int
    filename: str

@app.get("/api/models")
async def get_models():
    return {
        "groq": GROQ_MODEL_LIST,
        "google": GOOGLE_MODEL_LIST
    }

@app.get("/api/tools")
async def get_tools():
    tools = SearchTools.get_tool_list()
    return {"tools": [{"name": tool.name, "description": tool.description} for tool in tools]}

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Validate CSV
        df = pd.read_csv(file_path)
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "columns": df.columns.tolist(),
            "row_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/connect-gsheet")
async def connect_gsheet(sheet_url: str = Form(...)):
    try:
        # Initialize Google Sheets credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Open the sheet and get data
        sheet = client.open_by_url(sheet_url).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Save to CSV temporarily
        filename = f"gsheet_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = UPLOAD_DIR / filename
        df.to_csv(file_path, index=False)
        
        return {
            "message": "Google Sheet connected successfully",
            "filename": filename,
            "columns": df.columns.tolist(),
            "row_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/run-pipeline")
async def run_pipeline(request: SearchRequest):
    try:
        file_path = UPLOAD_DIR / request.filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        df = pd.read_csv(file_path)
        tools = SearchTools.get_tool_list()
        selected_tool = next((tool for tool in tools if tool.name == request.tool_name), None)
        
        if not selected_tool:
            raise HTTPException(status_code=400, detail="Invalid tool selection")
        
        pipeline = WebSearchPipeline(
            data_source=df,
            query_template=request.query_template,
            model_name=request.model_name,
            output_path=str(UPLOAD_DIR / "search_results.csv"),
            rate_limit=1.0,
            num_rows=request.num_rows,
            tools=[selected_tool],
        )
        
        results_df, results = pipeline.run()
        
        return {
            "results_df": results_df.to_dict(orient="records"),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)