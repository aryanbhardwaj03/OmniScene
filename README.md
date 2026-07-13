---
title: OmniScene
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.40.0
app_file: app.py
pinned: false
---

# OmniScene

Multi-Domain Visual Intelligence, Recognition & Health Screening Platform

## Features

- **Plant Species Recognition**: Identify plants using transfer learning.
- **Plant Disease Detection**: Analyze plants for diseases (e.g. Early Blight).
- **Explainable AI (Grad-CAM)**: Visualize what regions the model focused on.
- **Similarity Search**: Find similar previously analyzed images using DINOv2 embeddings and FAISS.

## Tech Stack

- **Backend**: FastAPI, PyTorch, HuggingFace Transformers, FAISS, PostgreSQL, SQLAlchemy
- **Frontend**: Next.js 15, React, TailwindCSS, Zustand
- **ML Models**: EfficientNet, ResNet (via HuggingFace PlantVillage fine-tunes), CLIP, DINOv2

## Running Locally

1. Create a `backend/.env` file with any overrides (optional).
2. Create a `frontend/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
3. Run `docker-compose up -d`
4. Visit `http://localhost:3000`

## Architecture

![architecture flow](https://via.placeholder.com/800x400?text=OmniScene+Architecture)

The backend uses a smart router that routes images through CLIP to determine the scene category, then dispatches to specialized models.
