import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

import uvicorn
from app.main import app

# Hugging Face ZeroGPU requires at least one @spaces.GPU function to exist, 
# otherwise its watchdog kills the container on startup.
try:
    import spaces
    @spaces.GPU
    def _dummy_gpu_function():
        pass
except ImportError:
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

