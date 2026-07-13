# 🌿 OmniScene

**Multi-Domain Visual Intelligence, Recognition & Health Screening Platform**

OmniScene is an advanced AI-powered platform that analyzes images of plants, animals, and scenes to identify species, detect diseases, provide management advice, and perform visual similarity searches.

## ✨ Features

- **Deep Image Analysis**: Upload images to automatically categorize the scene (plant, animal, etc.) and identify species (common and scientific names).
- **Health & Disease Screening**: Instantly detect diseases or health issues in plants and pets, providing a list of symptoms and actionable management advice.
- **Visual Similarity Search**: Uses advanced vector embeddings (DINOv2) to match your uploaded image against previously analyzed cases in real-time.
- **Interactive AI Chat**: Chat directly with an AI assistant about your specific image. Ask follow-up questions about plant care, pet health, or general scene details.
- **Analysis History**: Securely save and browse your past analysis results.

## 🛠️ Technology Stack

### Frontend (Vercel)
- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS & custom UI components
- **State Management**: Zustand
- **Analytics**: Vercel Analytics

### Backend (Hugging Face Spaces)
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Supabase) via SQLAlchemy & Asyncpg
- **Auth**: JWT-based authentication
- **AI Models**:
  - **Vision LLM**: Meta Llama-3 Vision (via Groq API) for high-speed, high-accuracy scene analysis and interactive chat.
  - **Embeddings**: Facebook DINOv2 (local inference) for highly accurate visual vector similarity.
  - **Vector Search**: FAISS (Facebook AI Similarity Search)

## 🚀 Architecture Overview

1. The **Next.js frontend** is deployed on Vercel and handles the user interface, state, and file uploads.
2. The **FastAPI backend** is hosted on Hugging Face Spaces (CPU Basic) to allow local inference of embedding models alongside REST endpoints.
3. When an image is uploaded, the backend simultaneously:
   - Queries the **Groq API** with Llama-3 Vision for structured JSON data (species, disease, management).
   - Runs **DINOv2** locally to generate a high-dimensional vector embedding.
   - Searches the **FAISS** index for visually similar past cases.
4. Data is stored securely in a **Supabase PostgreSQL** database.

## 💻 Local Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- A [Groq](https://console.groq.com) API Key
- A [Supabase](https://supabase.com/) PostgreSQL database

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/postgres
SECRET_KEY=your_super_secret_jwt_key
GROQ_API_KEY=gsk_your_groq_api_key
```

Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file in the `frontend` folder:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Run the frontend:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

## 📜 License
MIT License
