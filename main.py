"""
Cal.com Integration API for Vapi

This is the main application entry point that orchestrates all modules.
"""
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from routes import router

# Create FastAPI application
app = FastAPI(
    title="Cal.com Integration API for Vapi",
    description="API service for handling Cal.com operations via Vapi custom tools. Each endpoint processes Vapi tool calls and returns formatted, minimal responses.",
    version="1.0.0"
)

# Include all routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)