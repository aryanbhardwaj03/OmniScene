import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

import gradio as gr

# ZeroGPU requires @spaces.GPU to be wired to a Gradio event handler.
# Without this, the ZeroGPU watchdog kills the container on startup.
try:
    import spaces
    gpu_decorator = spaces.GPU
except ImportError:
    # Local development fallback (spaces package only exists on HF)
    gpu_decorator = lambda fn: fn

from app.main import app as fastapi_app


@gpu_decorator
def check_gpu_status():
    """Connected to Gradio button so ZeroGPU detects it at startup."""
    import torch
    if torch.cuda.is_available():
        return f"GPU available: {torch.cuda.get_device_name(0)}"
    return "Running on CPU (models will use CPU inference)"


# Build a minimal Gradio Blocks UI — ZeroGPU scans for @spaces.GPU
# functions that are wired to Gradio components. This satisfies that check.
with gr.Blocks(title="OmniScene API") as demo:
    gr.Markdown("# 🌿 OmniScene Backend API")
    gr.Markdown("API endpoints are available at **`/api/v1/`**")
    btn = gr.Button("Check GPU Status")
    status = gr.Textbox(label="Status")
    btn.click(fn=check_gpu_status, inputs=[], outputs=[status])

# Mount the Gradio UI at root "/" onto our FastAPI app.
# All /api/v1/* routes remain fully accessible.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
