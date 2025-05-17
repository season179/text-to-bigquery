from fastapi import FastAPI

app = FastAPI(title="BigQuery API")

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"}