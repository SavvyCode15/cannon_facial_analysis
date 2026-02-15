from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class FrameData(BaseModel):
    image: str # Base64 encoded
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None

class ScanRequest(BaseModel):
    frames: List[FrameData]
    config: Optional[Dict[str, Any]] = {}

class RealtimeRequest(BaseModel):
    image: str
    timestamp: float

class QualityMetrics(BaseModel):
    score: float
    lighting: str
    blur: str
    is_usable: bool

class FeatureResult(BaseModel):
    value: float
    confidence: Optional[float] = None
    unit: str = "ratio"
    status: str = "unknown"

class ScanResponse(BaseModel):
    success: bool
    scan_summary: Dict[str, Any]
    measurements: Dict[str, Any]
    golden_ratio_analysis: Optional[Dict[str, Any]] = None
    ai_recommendations: Optional[Dict[str, Any]] = None
    quality_metrics: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class RealtimeResponse(BaseModel):
    success: bool
    detected_angle: str
    angle_confidence: float = 0.0
    quality_score: float
    feedback: Dict[str, Any]
    landmarks_detected: bool
