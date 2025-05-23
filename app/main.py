from fastapi import FastAPI, Body
from dotenv import load_dotenv

# Load environment variables at application startup
load_dotenv()

app = FastAPI(title="BigQuery API")

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"}

@app.post("/text-to-sql")
async def text_to_sql(request: str = Body(...)):
    # Will implement the text-to-SQL logic later
    return {"result": "SQL query will be generated here"}