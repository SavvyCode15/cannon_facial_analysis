import math

class GoldenRatioAnalyzer:
    def __init__(self):
        self.GOLDEN_RATIO = 1.618
        
        # Scoring Standards: {feature_key: {'ideal': float, 'sigma': float, 'weight': float}}
        #
        # WEIGHTED SCORING PHILOSOPHY (PCA-like approach):
        # Major structural features (Tier 1) dictate the bulk of the score.
        # Minor features (Tier 3) act as small modifiers.
        # 
        # Tier 1 (Weight 3.0) - Core bone structure & harmony (User prioritized)
        # Tier 2 (Weight 1.5) - Important secondary features
        # Tier 3 (Weight 0.5) - Minor details
        
        self.SCORE_FLOOR = 5.0
        
        self.SCORING_STANDARDS = {
            # ── Tier 1: Major Harmony & Bone Structure (Weight 3.0) ──────────
            "ipd_mm":                   {"ideal": 63.0,  "sigma": 4.0,  "weight": 3.0},
            "jaw_cheek_ratio":          {"ideal": 0.78,  "sigma": 0.08, "weight": 3.0}, # Jawline
            "gonial_angle":             {"ideal": 125.0, "sigma": 8.0,  "weight": 3.0},
            "zygomatic_projection":     {"ideal": 1.45,  "sigma": 0.10, "weight": 3.0}, # Face width / Eye width
            "chin_projection_mm":       {"ideal": 5.0,   "sigma": 3.0,  "weight": 3.0}, 
            "midface_projection_mm":    {"ideal": 15.0,  "sigma": 5.0,  "weight": 3.0}, # Forward growth
            "midface_ratio":            {"ideal": 1.0,   "sigma": 0.10, "weight": 3.0},
            "esr":                      {"ideal": 0.46,  "sigma": 0.04, "weight": 3.0},
            "facial_convexity":         {"ideal": 170.0, "sigma": 6.0,  "weight": 3.0},
            
            # ── Tier 2: Secondary Features (Weight 1.5) ──────────────────────
            "symmetry_score":           {"ideal": 100.0, "sigma": 7.75, "weight": 1.5},
            "canthal_tilt_left":        {"ideal": 7.0,   "sigma": 3.0,  "weight": 1.5},
            "canthal_tilt_right":       {"ideal": 7.0,   "sigma": 3.0,  "weight": 1.5},
            "cheekbone_prominence":     {"ideal": 1.15,  "sigma": 0.10, "weight": 1.5},
            "face_width_height_ratio":  {"ideal": 0.78,  "sigma": 0.08, "weight": 1.5},
            "mid_lower_ratio":          {"ideal": 1.0,   "sigma": 0.10, "weight": 1.5},
            
            # ── Tier 3: Minor Details (Weight 0.5) ───────────────────────────
            "nose_width_ratio":         {"ideal": 0.25,  "sigma": 0.04, "weight": 0.5},
            "chin_philtrum_ratio":      {"ideal": 2.5,   "sigma": 0.4,  "weight": 0.5},
            "nasolabial_angle":         {"ideal": 100.0, "sigma": 8.0,  "weight": 0.5},
            "mentolabial_angle":        {"ideal": 125.0, "sigma": 12.0, "weight": 0.5},
            "nose_tip_angle":           {"ideal": 85.0,  "sigma": 8.0,  "weight": 0.5},
            "forehead_slope":           {"ideal": 10.0,  "sigma": 6.0,  "weight": 0.5},
        }
    
    def calculate_normalized_score(self, value: float, ideal: float, sigma: float) -> float:
        """
        Score (5.0–10.0) using floored Gaussian.
        """
        if sigma <= 0:
            return self.SCORE_FLOOR
        exponent = -((value - ideal) ** 2) / (2 * sigma ** 2)
        gaussian = math.exp(exponent)
        return self.SCORE_FLOOR + (10.0 - self.SCORE_FLOOR) * gaussian

    def analyze(self, measurements: dict) -> dict:
        """
        Compare measurements against ideals and generate weighted normalized scores.
        """
        analysis = {
            "scores": {},
            "total_score": 0,
            "average_score": 0
        }
        
        total_weighted_score = 0
        total_weight = 0

        for key, value in measurements.items():
            standard = self.SCORING_STANDARDS.get(key)
            if standard is None:
                continue
            
            # Skip zero or near-zero values for mm measurements (uncalibrated)
            if isinstance(value, (int, float)) and abs(value) < 1e-5:
                # If it's a projection value that wasn't calibrated, skip it so we don't penalize
                continue
            
            score = self.calculate_normalized_score(value, standard['ideal'], standard['sigma'])
            score = round(min(10.0, max(self.SCORE_FLOOR, score)), 1)
            
            # Apply weight
            weight = standard.get('weight', 1.0)
            total_weighted_score += (score * weight)
            total_weight += weight
            
            # Rating labels for 5-10 scale
            if score >= 9.5:    rating = "Ideal"
            elif score >= 8.5:  rating = "Excellent"
            elif score >= 7.5:  rating = "Good"
            elif score >= 6.5:  rating = "Above Average"
            elif score >= 5.5:  rating = "Average"
            else:               rating = "Below Average"
            
            analysis["scores"][key] = {
                "value": value,
                "ideal": standard['ideal'],
                "score": score,
                "rating": rating,
                "weight": weight
            }
            
        if total_weight > 0:
            # The simple total score (unweighted) isn't as useful anymore, 
            # but we can return the weighted average as the true "average_score"
            final_score = round(total_weighted_score / total_weight, 1)
            analysis["total_score"] = round(total_weighted_score, 1) # Just for legacy compatibility if needed
            analysis["average_score"] = final_score

        return analysis
