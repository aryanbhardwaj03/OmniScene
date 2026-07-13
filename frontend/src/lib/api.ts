import { AnalysisResponse } from '@/types/analysis';
import { useAuthStore } from './store';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

function getAuthHeaders(): Record<string, string> {
  const token = useAuthStore.getState().token;
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

export async function analyzeImage(file: File): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: {
      ...getAuthHeaders()
    },
    body: formData,
  });

  if (!res.ok) {
    throw new Error('Failed to analyze image');
  }

  return res.json();
}

export async function getHistory(page: number = 1, size: number = 20) {
  const res = await fetch(`${API_BASE}/history?page=${page}&size=${size}`, {
    headers: {
      ...getAuthHeaders()
    }
  });
  
  if (!res.ok) {
    if (res.status === 401) {
      useAuthStore.getState().logout();
    }
    throw new Error('Failed to fetch history');
  }

  return res.json();
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export async function sendChatMessage(
  analysisId: string, 
  message: string, 
  history: ChatMessage[] = [],
  onChunk?: (chunk: string) => void
) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({
      analysis_id: analysisId,
      message,
      history,
    }),
  });

  if (!res.ok) {
    throw new Error('Failed to send chat message');
  }

  // If a callback is provided, we read the stream
  if (onChunk && res.body) {
    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;
    let fullResponse = '';

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) {
        const chunkValue = decoder.decode(value, { stream: !done });
        fullResponse += chunkValue;
        onChunk(chunkValue);
      }
    }
    return { reply: fullResponse };
  }

  // Fallback for non-streaming (shouldn't happen now, but good to keep)
  const text = await res.text();
  return { reply: text };
}
