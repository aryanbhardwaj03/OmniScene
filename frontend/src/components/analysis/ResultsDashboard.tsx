"use client"

import { useRef, useState } from 'react';
import { AnalysisResponse } from '@/types/analysis';
import ConfidenceBadge from './ConfidenceBadge';
import GradCAMViewer from './GradCAMViewer';
import SimilarResults from './SimilarResults';
import ImageChat from './ImageChat';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

interface Props {
  result: AnalysisResponse;
  imageUrl: string;
}

export default function ResultsDashboard({ result, imageUrl }: Props) {
  const [isExporting, setIsExporting] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  // We'll focus on the first detection for the dashboard
  const detection = result.detections[0];
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  
  // Format the gradcam URL if it exists
  const backendBase = API_BASE.replace('/api/v1', '');
  
  const gradcamUrl = detection?.explainability?.gradcam_url 
    ? `${backendBase}${detection.explainability.gradcam_url}` 
    : null;

  const handleExportPDF = async () => {
    if (!reportRef.current) return;
    setIsExporting(true);
    
    try {
      const canvas = await html2canvas(reportRef.current, { scale: 2, useCORS: true });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`OmniScene-Report-${result.id.substring(0, 8)}.pdf`);
    } catch (err) {
      console.error('Failed to generate PDF:', err);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Top Meta Bar */}
      <div className="glass-card p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">Scene Category:</span>
          <span className="px-3 py-1 bg-secondary rounded-full text-sm font-medium capitalize">
            {result.scene_category}
          </span>
          <span className="text-xs text-muted-foreground">({(result.scene_confidence * 100).toFixed(1)}%)</span>
        </div>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span>Processed in <span className="font-mono text-foreground">{result.processing_time_ms}ms</span></span>
          <button 
            onClick={handleExportPDF} 
            disabled={isExporting}
            className="flex items-center gap-2 bg-primary/10 hover:bg-primary/20 text-primary px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
          >
            {isExporting ? 'Generating PDF...' : 'Download PDF Report'}
          </button>
        </div>
      </div>

      <div ref={reportRef} className="flex flex-col gap-6 p-2 -m-2 bg-background">

      {detection?.category === 'plant' && detection.species && detection.disease ? (
        <>
          {/* Main Plant Results */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Species Card */}
            <div className="glass-card p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22c4-4 4-10 4-14 0-4-4-4-4-4s-4 0-4 4c0 4 0 10 4 14z"/></svg>
              </div>
              <h3 className="text-sm text-muted-foreground uppercase tracking-wider font-semibold mb-1">Identified Species</h3>
              <h2 className="text-2xl font-bold mb-1">{detection.species.common_name}</h2>
              <p className="text-sm italic text-muted-foreground mb-4">{detection.species.scientific_name}</p>
              
              <div className="mt-auto">
                <ConfidenceBadge level={detection.species.confidence_level} score={detection.species.confidence} />
              </div>
            </div>

            {/* Disease Card */}
            <div className={`glass-card p-6 relative overflow-hidden ${
              detection.disease.name.toLowerCase() === 'healthy' 
                ? 'border-emerald-500/30 bg-emerald-500/5' 
                : 'border-amber-500/30 bg-amber-500/5'
            }`}>
              <h3 className="text-sm text-muted-foreground uppercase tracking-wider font-semibold mb-1">Health Status</h3>
              <h2 className="text-2xl font-bold mb-4">{detection.disease.name}</h2>
              
              <div className="space-y-4">
                <div>
                  <ConfidenceBadge level={detection.disease.confidence_level} score={detection.disease.confidence} />
                </div>
                
                {detection.disease.name.toLowerCase() !== 'healthy' && detection.disease.management && detection.disease.management.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium mb-1">Management:</h4>
                    <ul className="text-sm text-muted-foreground list-disc list-inside space-y-1">
                      {detection.disease.management.map((m, i) => <li key={i}>{m}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      ) : detection ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-card p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M2 12h4l3-9 5 18 3-9h5"/></svg>
            </div>
            <h3 className="text-sm text-muted-foreground uppercase tracking-wider font-semibold mb-1">Analysis Result</h3>
            <h2 className="text-2xl font-bold mb-1">{detection.species?.common_name || "Unknown"}</h2>
            <p className="text-sm italic text-muted-foreground mb-4">{detection.species?.scientific_name || ""}</p>
            
            {detection.species && (
              <div className="mt-auto">
                <ConfidenceBadge level={detection.species.confidence_level} score={detection.species.confidence} />
              </div>
            )}
          </div>
          
          {detection.disease && (
            <div className="glass-card p-6 relative overflow-hidden bg-secondary/10">
              <h3 className="text-sm text-muted-foreground uppercase tracking-wider font-semibold mb-1">Health Status</h3>
              <h2 className="text-xl font-bold mb-4">{detection.disease.name}</h2>
              <div className="mt-auto">
                <ConfidenceBadge level={detection.disease.confidence_level} score={detection.disease.confidence} />
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-2">Unsupported Category</h2>
          <p className="text-muted-foreground">
            The image was classified as <strong>{result.scene_category}</strong>, which is currently not supported by the specialized analysis models.
          </p>
        </div>
      )}

      {/* Similarity Search Section */}
      {result.similar_images && result.similar_images.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-semibold mb-4">Visually Similar Cases</h3>
          <p className="text-sm text-muted-foreground mb-6">Found in vector database using DINOv2 embeddings.</p>
          <SimilarResults images={result.similar_images} backendBase={backendBase} />
        </div>
      )}

      {/* VLM Image Chat Integration */}
      {result.id && (
        <ImageChat analysisId={result.id} />
      )}
      </div>
    </div>
  );
}
