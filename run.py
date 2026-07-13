import os
import sys

# Add the backend directory to the Python path so it can find the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

import uvicorn
import gradio as gr
from app.main import app as fastapi_app

# Hugging Face's Gradio SDK expects a Gradio UI at the root (/) to pass its health checks.
# If it doesn't find one, it sometimes kills the container.
# We create a simple dummy Gradio app and mount our FastAPI app to it.
def api_status():
    return "OmniScene API is running successfully on Hugging Face Spaces!"

demo = gr.Interface(
    fn=api_status, 
    inputs=[], 
    outputs="text",
    title="OmniScene Backend API"
)

# Mount the Gradio app ONTO our FastAPI app at the root path
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

