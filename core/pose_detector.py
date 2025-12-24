import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_confidence=0.5, tracking_confidence=0.5):
        """
        Initialize the MediaPipe Pose detector.
        """
        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.complexity,
            smooth_landmarks=self.smooth_landmarks,
            enable_segmentation=self.enable_segmentation,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def find_pose(self, img, draw=True):
        """
        Processes an image/frame to detect the pose.
        Returns the image with landmarks drawn (if draw=True) and the results object.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(
                    img, 
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
        return img

    def get_position(self, img, draw=True):
        """
        Extracts landmark positions from the processed results.
        Returns a list of landmarks [id, x, y, z, visibility].
        """
        lm_list = []
        if self.results.pose_landmarks:
            h, w, c = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # cx, cy are pixel coordinates
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy, lm.z, lm.visibility])
                
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lm_list

    def get_world_landmarks(self):
        """
        Returns the world 3D landmarks (meters).
        Useful for calculating real-world angles/distances if needed.
        """
        if self.results.pose_world_landmarks:
            return self.results.pose_world_landmarks.landmark
        return None
