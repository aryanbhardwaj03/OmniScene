"use client"

import { SimilarImage } from "@/types/analysis";

interface Props {
  images: SimilarImage[];
  backendBase: string;
}

export default function SimilarResults({ images, backendBase }: Props) {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4 snap-x">
      {images.map((img, idx) => {
        const similarityScore = (img.similarity * 100).toFixed(1);
        const thumbUrl = img.thumbnail_url.startsWith('http') 
          ? img.thumbnail_url 
          : `${backendBase}${img.thumbnail_url}`;
          
        return (
          <div key={idx} className="shrink-0 w-48 bg-secondary/20 rounded-lg overflow-hidden border snap-start group cursor-pointer hover:border-primary/50 transition-colors">
            <div className="h-32 bg-black/20 flex items-center justify-center overflow-hidden">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img 
                src={thumbUrl} 
                alt="Similar case" 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM1NTViNjUiIHN0cm9rZS13aWR0aD0iMSIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHJlY3QgeD0iMyIgeT0iMyIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiByeD0iMiIgcnk9IjIiLz48Y2lyY2xlIGN4PSI4LjUiIGN5PSI4LjUiIHI9IjEuNSIvPjxwb2x5bGluZSBwb2ludHM9IjIxIDE1IDE2IDEwIDUgMjEiLz48L3N2Zz4=';
                }}
              />
            </div>
            <div className="p-3">
              <div className="text-xs text-muted-foreground mb-1 font-mono">{img.id.split('-')[0]}</div>
              <div className="flex items-center gap-1.5 text-sm font-medium">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                {similarityScore}% Match
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
