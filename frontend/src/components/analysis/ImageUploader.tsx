"use client"

import { useState, useCallback } from 'react';

interface Props {
  onAnalyze: (file: File) => void;
  isLoading: boolean;
}

export default function ImageUploader({ onAnalyze, isLoading }: Props) {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (newFile: File) => {
    if (!newFile.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }
    setFile(newFile);
    
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(newFile);
  };

  return (
    <div className="w-full flex flex-col gap-4">
      <div 
        className={`relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl transition-all ${
          dragActive ? 'border-primary bg-primary/5' : 'border-border/60 hover:border-border hover:bg-accent/50'
        } ${previewUrl ? 'p-2' : 'p-6'}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          accept="image/*"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
          onChange={handleChange}
          disabled={isLoading}
        />
        
        {previewUrl ? (
          <div className="relative w-full h-full rounded-lg overflow-hidden flex items-center justify-center bg-black/20">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={previewUrl} alt="Preview" className="max-h-full max-w-full object-contain" />
            <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
              <span className="text-white font-medium">Click or drag to change image</span>
            </div>
          </div>
        ) : (
          <div className="text-center pointer-events-none">
            <svg className="mx-auto h-12 w-12 text-muted-foreground/60 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <p className="text-lg font-medium text-foreground/80">Drag and drop your image here</p>
            <p className="text-sm text-muted-foreground mt-1">or click to browse from your device</p>
          </div>
        )}
      </div>

      <button
        onClick={() => file && onAnalyze(file)}
        disabled={!file || isLoading}
        className={`premium-button w-full h-14 text-lg ${
          !file 
            ? 'opacity-50 cursor-not-allowed saturate-0' 
            : isLoading
              ? 'opacity-80 cursor-wait'
              : ''
        }`}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analyzing Image...
          </>
        ) : (
          <>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Analyze Image
          </>
        )}
      </button>
    </div>
  );
}
