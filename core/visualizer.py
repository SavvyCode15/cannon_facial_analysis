import cv2
import numpy as np
import mediapipe as mp
from typing import Optional

class Visualizer:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh

        # Custom mesh style — cyan/electric blue tessellation
        self.mesh_style = self.mp_drawing.DrawingSpec(
            color=(255, 255, 0),  # Cyan in RGB
            thickness=1,
            circle_radius=0
        )
        
        # Contour style — bright green for eyes, lips, face oval
        self.contour_style = self.mp_drawing.DrawingSpec(
            color=(0, 255, 128),  # Bright green in RGB
            thickness=1,
            circle_radius=0
        )

    def draw_mesh(self, image: np.ndarray, landmarks) -> np.ndarray:
        """
        Draws the face mesh tessellation and contours on the image.
        Args:
            image: RGB image (numpy array)
            landmarks: MediaPipe normalized landmarks
            
        Returns:
            Image with mesh drawn (RGB)
        """
        annotated_image = image.copy()
        
        # Draw tessellation (the "mesh" look) — cyan lines
        self.mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mesh_style
        )
        
        # Draw contours (eyes, lips, face oval) — bright green
        self.mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.contour_style
        )
        
        return annotated_image

    def draw_pose_info(self, image: np.ndarray, yaw: float, pitch: float, roll: float) -> np.ndarray:
        """
        Draws head pose angles on the image.
        """
        annotated_image = image.copy()
        
        text = f"Y: {int(yaw)} P: {int(pitch)} R: {int(roll)}"
        cv2.putText(annotated_image, text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    
        return annotated_image

# Singleton instance
visualizer = Visualizer()
