"use client"

import { useState } from 'react';
import ImageUploader from '@/components/analysis/ImageUploader';
import ResultsDashboard from '@/components/analysis/ResultsDashboard';
import { analyzeImage } from '@/lib/api';
import { AnalysisResponse } from '@/types/analysis';

export default function AnalyzePage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const handleAnalyze = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);
    setResult(null);
    
    // Create local object URL for immediate display
    const objectUrl = URL.createObjectURL(file);
    setUploadedImage(objectUrl);
    
    try {
      const response = await analyzeImage(file);
      setResult(response);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze image. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl flex-1 flex flex-col">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Analyze Image</h1>
        <p className="text-muted-foreground">Upload a plant or scene image to run it through the OmniScene AI pipeline.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 flex-1">
        {/* Left Column: Uploader */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <div className="glass-card p-6 sticky top-24">
            <h2 className="text-xl font-semibold mb-4">Input</h2>
            <ImageUploader onAnalyze={handleAnalyze} isLoading={isAnalyzing} />
            
            {error && (
              <div className="mt-4 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive-foreground">
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Results */}
        <div className="lg:col-span-8 flex flex-col">
          {isAnalyzing ? (
            <div className="glass-card flex-1 flex flex-col items-center justify-center p-12 min-h-[400px]">
              <div className="relative w-24 h-24 mb-6">
                <div className="absolute inset-0 rounded-full border-t-2 border-primary animate-spin"></div>
                <div className="absolute inset-2 rounded-full border-r-2 border-emerald-400 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                <div className="absolute inset-4 rounded-full border-b-2 border-blue-400 animate-spin" style={{ animationDuration: '3s' }}></div>
              </div>
              <h3 className="text-xl font-semibold mb-2 animate-pulse">Running AI Pipeline...</h3>
              <p className="text-muted-foreground text-center max-w-md">
                Routing image through CLIP, running specialist models, generating Grad-CAM explanations, and searching vector space.
              </p>
            </div>
          ) : result && uploadedImage ? (
            <ResultsDashboard result={result} imageUrl={uploadedImage} />
          ) : (
            <div className="glass-card flex-1 flex flex-col items-center justify-center p-12 text-muted-foreground min-h-[400px] border-dashed">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="mb-4 opacity-50"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
              <h3 className="text-lg font-medium mb-1 text-foreground">Waiting for input</h3>
              <p className="text-sm text-center">Upload an image on the left to see results here.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
