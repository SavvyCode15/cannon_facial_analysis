import math

class GoldenRatioAnalyzer:
    def __init__(self):
        self.GOLDEN_RATIO = 1.618
        
        # Scoring Standards: {feature_key: {'ideal': float, 'sigma': float}}
        #
        # NORMALIZATION PHILOSOPHY:
        # - Score floor of 5.0: every detected feature starts at minimum 5.
        # - Sigma calibrated so that a value ~15% off ideal scores ~6.5,
        #   a value ~5% off ideal scores ~9+, and exact ideal = 10.
        # - Formula: score = 5 + 5 * exp(-(x-ideal)^2 / (2 * sigma^2))
        # - Near-zero values (uncalibrated mm) are skipped automatically.
        
        self.SCORE_FLOOR = 5.0
        
        self.SCORING_STANDARDS = {
            # ── Front View ─────────────────────────────────────────────────────
            
            # Midface ratio: 10-15% deviation = ~6.5. sigma=0.097
            "midface_ratio":            {"ideal": 1.0,   "sigma": 0.10},
            
            # Canthal tilt: most people 0-10°. 4° off ideal → ~7.1. sigma=3
            "canthal_tilt_left":        {"ideal": 7.0,   "sigma": 3.0},
            "canthal_tilt_right":       {"ideal": 7.0,   "sigma": 3.0},
            
            # IPD: narrow by 4mm → ~8.5. sigma=4
            "ipd_mm":                   {"ideal": 63.0,  "sigma": 4.0},
            
            # Eye-Set Ratio: off by 0.04 (9% off) → ~6.5. sigma=0.04
            "esr":                      {"ideal": 0.46,  "sigma": 0.04},
            
            # Jaw-to-cheek: off by 0.08 → ~6.5. sigma=0.08
            "jaw_cheek_ratio":          {"ideal": 0.78,  "sigma": 0.08},
            
            # Nose width: off by 0.04 → ~6.5
            "nose_width_ratio":         {"ideal": 0.25,  "sigma": 0.04},
            
            # Face width/height: off by 0.08 → ~6.5
            "face_width_height_ratio":  {"ideal": 0.78,  "sigma": 0.08},
            
            # Symmetry: 88 score → 6.5, 95 → 9.1, 100 → 10. sigma=7.75
            "symmetry_score":           {"ideal": 100.0, "sigma": 7.75},
            
            # Chin-philtrum: off by 0.4 → ~7. sigma=0.4
            "chin_philtrum_ratio":      {"ideal": 2.5,   "sigma": 0.4},
            
            # Mid/lower face: off by 0.1 → ~7.1. sigma=0.1
            "mid_lower_ratio":          {"ideal": 1.0,   "sigma": 0.10},
            
            # Cheekbone prominence: off by 0.1 → ~7.1
            "cheekbone_prominence":     {"ideal": 1.15,  "sigma": 0.10},
            
            # ── Profile View ───────────────────────────────────────────────────
            
            # Facial convexity: off by 6° → ~7. sigma=6
            "facial_convexity":         {"ideal": 170.0, "sigma": 6.0},
            
            # Nasolabial angle: off by 8° → ~7. sigma=8
            "nasolabial_angle":         {"ideal": 100.0, "sigma": 8.0},
            
            # Mentolabial angle: off by 12° → ~7. sigma=12
            "mentolabial_angle":        {"ideal": 125.0, "sigma": 12.0},
            
            # Gonial angle: off by 8° → ~7. sigma=8
            "gonial_angle":             {"ideal": 125.0, "sigma": 8.0},
            
            # Nose tip angle: off by 8° → ~7. sigma=8
            "nose_tip_angle":           {"ideal": 85.0,  "sigma": 8.0},
            
            # Forehead slope: off by 6° → ~7. sigma=6
            "forehead_slope":           {"ideal": 10.0,  "sigma": 6.0},
        }
    
    def calculate_normalized_score(self, value: float, ideal: float, sigma: float) -> float:
        """
        Score (5.0–10.0) using floored Gaussian.
        
        score = FLOOR + (10 - FLOOR) * exp(-(x-ideal)^2 / (2*sigma^2))
        
        - Exact ideal → 10.0
        - Moderate deviation (~15%) → 6.0-7.0  (Average)
        - Far from ideal → 5.0  (floor, never less)
        """
        if sigma <= 0:
            return self.SCORE_FLOOR
        exponent = -((value - ideal) ** 2) / (2 * sigma ** 2)
        gaussian = math.exp(exponent)
        return self.SCORE_FLOOR + (10.0 - self.SCORE_FLOOR) * gaussian

    def analyze(self, measurements: dict) -> dict:
        """
        Compare measurements against ideals and generate normalized scores.
        measurements: dict of feature_name -> value (float)
        """
        analysis = {
            "scores": {},
            "total_score": 0,
            "average_score": 0
        }
        
        total_score_sum = 0
        count = 0

        for key, value in measurements.items():
            standard = self.SCORING_STANDARDS.get(key)
            if standard is None:
                continue
            
            # Skip zero or near-zero values — these are uncalibrated mm measurements
            # (e.g. midface_projection_mm returns 0 when calibration_scale=0)
            if isinstance(value, (int, float)) and abs(value) < 1e-5:
                continue
            
            score = self.calculate_normalized_score(value, standard['ideal'], standard['sigma'])
            score = round(min(10.0, max(self.SCORE_FLOOR, score)), 1)
            
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
                "rating": rating
            }
            
            total_score_sum += score
            count += 1
        
        if count > 0:
            analysis["total_score"] = round(total_score_sum, 1)
            analysis["average_score"] = round(total_score_sum / count, 1)

        return analysis
