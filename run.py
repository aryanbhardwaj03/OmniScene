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


# ---- Mount our FastAPI routes onto Gradio's internal FastAPI app ----
# Gradio's Blocks exposes its internal FastAPI app via demo.app
# We add CORS, static files, and all our API routes to it.

demo.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.STATIC_DIR, exist_ok=True)
demo.app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
demo.app.include_router(api_router, prefix=settings.API_V1_STR)


@demo.app.get("/health")
def health_check():
    return {"status": "ok"}


@demo.app.on_event("shutdown")
async def shutdown_event():
    await model_registry.unload_all()


# ---- Launch via Gradio (ZeroGPU hooks into this) ----
# DO NOT use uvicorn.run() — ZeroGPU requires demo.launch()
demo.launch(server_name="0.0.0.0", server_port=7860)
