"use client"

import { useState } from "react";

interface Props {
  originalImage: string;
  gradcamImage: string | null;
}

export default function GradCAMViewer({ originalImage, gradcamImage }: Props) {
  const [opacity, setOpacity] = useState(70);
  const [viewMode, setViewMode] = useState<'overlay' | 'original' | 'heatmap'>('overlay');

  if (!gradcamImage) {
    return (
      <div className="bg-secondary/50 rounded-lg p-8 text-center text-muted-foreground border border-dashed">
        Grad-CAM heatmap could not be generated for this image.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-3 bg-secondary/30 rounded-lg">
        <div className="flex bg-background rounded-md p-1 border">
          <button 
            className={`px-3 py-1 text-xs font-medium rounded-sm transition-colors ${viewMode === 'original' ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'}`}
            onClick={() => setViewMode('original')}
          >
            Original
          </button>
          <button 
            className={`px-3 py-1 text-xs font-medium rounded-sm transition-colors ${viewMode === 'overlay' ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'}`}
            onClick={() => setViewMode('overlay')}
          >
            Overlay
          </button>
          <button 
            className={`px-3 py-1 text-xs font-medium rounded-sm transition-colors ${viewMode === 'heatmap' ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'}`}
            onClick={() => setViewMode('heatmap')}
          >
            Heatmap
          </button>
        </div>
        
        {viewMode === 'overlay' && (
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-muted-foreground">Opacity:</span>
            <input 
              type="range" 
              min="0" max="100" 
              value={opacity} 
              onChange={(e) => setOpacity(parseInt(e.target.value))}
              className="w-32 accent-primary"
            />
            <span className="text-xs font-mono w-8">{opacity}%</span>
          </div>
        )}
      </div>

      {/* Viewer */}
      <div className="relative aspect-video bg-black rounded-lg overflow-hidden border">
        {/* Base Layer */}
        <div className="absolute inset-0 flex items-center justify-center">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img 
            src={viewMode === 'heatmap' ? gradcamImage : originalImage} 
            alt="Base" 
            className="max-w-full max-h-full object-contain"
          />
        </div>

        {/* Overlay Layer */}
        {viewMode === 'overlay' && (
          <div 
            className="absolute inset-0 flex items-center justify-center transition-opacity"
            style={{ opacity: opacity / 100 }}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img 
              src={gradcamImage} 
              alt="Grad-CAM Overlay" 
              className="max-w-full max-h-full object-contain mix-blend-screen"
            />
          </div>
        )}
      </div>
    </div>
  );
}
