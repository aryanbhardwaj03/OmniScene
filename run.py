import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

# ZeroGPU: must import spaces BEFORE gradio for proper hook registration
import spaces
import gradio as gr

# Import backend components
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.router import api_router
from app.ml.registry import model_registry


# ---- ZeroGPU-compatible GPU function ----
# Must use @spaces.GPU directly (not via variable) and wire to a Gradio component.
# ZeroGPU scans for this pattern to know the app needs GPU access.
@spaces.GPU
def check_gpu_status():
    import torch
    if torch.cuda.is_available():
        return f"GPU available: {torch.cuda.get_device_name(0)}"
    return "Running on CPU (models will use CPU inference)"


# ---- Gradio UI (required for ZeroGPU) ----
with gr.Blocks(title="OmniScene API") as demo:
    gr.Markdown("# 🌿 OmniScene Backend API")
    gr.Markdown("REST API: **`/api/v1/`** &nbsp;|&nbsp; Docs: **`/docs`**")
    btn = gr.Button("Check GPU Status", variant="primary")
    status = gr.Textbox(label="Status", interactive=False)
    btn.click(fn=check_gpu_status, inputs=[], outputs=[status])


# ---- Create custom FastAPI app ----
from app.main import app

# ---- Mount Gradio into FastAPI ----
# Exposing 'app' allows Hugging Face Spaces to serve the FastAPI app directly
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
