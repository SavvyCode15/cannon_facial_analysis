import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional, Any

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process_image(self, image: np.ndarray) -> Optional[Any]:
        """
        Process an image and return face landmarks.
        Image should be in RGB format.
        """
        results = self.face_mesh.process(image)
        if not results.multi_face_landmarks:
            return None
        return results.multi_face_landmarks[0]

    def get_landmarks_as_array(self, landmarks, image_shape) -> np.ndarray:
        """
        Convert landmarks to a numpy array of (x, y, z) coordinates.
        """
        h, w = image_shape[:2]
        landmark_array = np.array([
            [lm.x * w, lm.y * h, lm.z * w] 
            for lm in landmarks.landmark
        ])
        return landmark_array
