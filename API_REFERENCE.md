# API Reference

**Base URL**: `http://<YOUR_IP>:8000/api`

## 1. Check Angle (Realtime)
**Call this repeatedly while scanning.**
*   **POST** `/scan/analyze-realtime`
*   **Send**:
    ```json
    {
      "image": "base64_string_of_image",
      "timestamp": 12345.6
    }
    ```
*   **Get**:
    ```json
    {
      "detected_angle": "front",  // or "left_profile", "right_profile"
      "feedback": { "message": "Angle: Front" }
    }
    ```

---

## 2. Get Analysis (Final Result)
**Call this ONCE when scan is done.**
*   **POST** `/scan/analyze`
*   **Send** (List of all frames):
    ```json
    {
      "frames": [
        { "image": "base64...", "timestamp": 100.1 },
        { "image": "base64...", "timestamp": 100.2 }
        // ... all captured frames
      ]
    }
    ```
*   **Get** (The Features & Scores):
    ```json
    {
      "scan_summary": { "overall_score": 8.5 },
      "measurements": {
        "front_view": {
          "canthal_tilt_left": { "value": 6.5, "score": 9.0, "rating": "Ideal" },
          "symmetry_score": { "value": 85.0 }
        }
      },
      "ai_recommendations": { "summary": "...", "recommendations": [] }
    }
    ```
