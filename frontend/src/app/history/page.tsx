"use client"

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getHistory } from '@/lib/api';
import { useAuthStore } from '@/lib/store';


// Simple types matching what we send from backend v1
interface HistoryItem {
  id: string;
  timestamp: string;
  scene_category: string;
  scene_confidence: number;
  detections: any[];
  processing_time_ms: number;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  const backendBase = API_BASE.replace('/api/v1', '');
  const router = useRouter();
  const { token } = useAuthStore();

  useEffect(() => {
    if (!token) {
      router.push('/login');
      return;
    }

    const fetchHistory = async () => {

      try {
        const data = await getHistory(1, 50);
        setHistory(data.items);
      } catch (err) {
        console.error(err);
        setError("Failed to load history.");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchHistory();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl flex-1">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Analysis History</h1>
        <p className="text-muted-foreground">View your past image analyses and their results.</p>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center p-12">
          <svg className="animate-spin h-8 w-8 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : error ? (
        <div className="p-4 bg-destructive/10 text-destructive border border-destructive/20 rounded-lg">
          {error}
        </div>
      ) : history.length === 0 ? (
        <div className="glass-card p-12 text-center text-muted-foreground border-dashed">
          No history found. Try analyzing an image first!
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {history.map((item) => (
            <div key={item.id} className="glass-card rounded-lg overflow-hidden group hover:border-primary/50 transition-colors">
              <div className="aspect-square bg-black/20 overflow-hidden relative">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img 
                  src={`${backendBase}/static/uploads/${item.id}.jpg`} 
                  alt="Analysis" 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM1NTViNjUiIHN0cm9rZS13aWR0aD0iMSIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHJlY3QgeD0iMyIgeT0iMyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiByeD0iMiIgcnk9IjIiLz48Y2lyY2xlIGN4PSI4LjUiIGN5PSI4LjUiIHI9IjEuNSIvPjxwb2x5bGluZSBwb2ludHM9IjIxIDE1IDE2IDEwIDUgMjEiLz48L3N2Zz4=';
                  }}
                />
                <div className="absolute top-2 right-2 px-2 py-1 bg-black/60 backdrop-blur-sm rounded text-xs font-medium text-white capitalize">
                  {item.scene_category}
                </div>
              </div>
              <div className="p-4">
                <div className="text-xs text-muted-foreground mb-2">
                  {new Date(item.timestamp).toLocaleString()}
                </div>
                {item.detections && item.detections[0] && item.detections[0].disease ? (
                  <>
                    <h3 className="font-semibold text-lg line-clamp-1">{item.detections[0].disease.name}</h3>
                    <p className="text-sm text-muted-foreground line-clamp-1">{item.detections[0].species.common_name}</p>
                  </>
                ) : (
                  <h3 className="font-semibold text-lg line-clamp-1">No Specifics</h3>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
