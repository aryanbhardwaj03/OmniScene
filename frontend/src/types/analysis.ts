export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW' | 'UNKNOWN';

export interface ImageMeta {
  width: number;
  height: number;
  format: string;
}

export interface SpeciesInfo {
  common_name: string;
  scientific_name: string;
  confidence: number;
  confidence_level: ConfidenceLevel;
}

export interface DiseaseInfo {
  name: string;
  scientific_name?: string;
  confidence: number;
  confidence_level: ConfidenceLevel;
  severity?: string;
  symptoms: string[];
  management: string[];
}

export interface ExplainabilityInfo {
  gradcam_url?: string;
  top_regions: string[];
}

export interface BoundingBox {
  x_min: number;
  y_min: number;
  x_max: number;
  y_max: number;
}

export interface DetectionResult {
  category: string;
  species?: SpeciesInfo;
  disease?: DiseaseInfo;
  explainability?: ExplainabilityInfo;
  bounding_box?: BoundingBox;
}

export interface SimilarImage {
  id: string;
  similarity: number;
  thumbnail_url: string;
}

export interface AnalysisResponse {
  id: string;
  timestamp: string;
  image_size: ImageMeta;
  scene_category: string;
  scene_confidence: number;
  detections: DetectionResult[];
  similar_images: SimilarImage[];
  processing_time_ms: number;
  model_versions: Record<string, string>;
}
