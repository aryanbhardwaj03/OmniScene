import os
import sys

# Add the backend directory to the Python path so it can find the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.main import app

# Hugging Face Gradio SDK automatically detects the `app` object if it's a FastAPI instance
# and serves it for us! We do NOT need to run uvicorn manually.

