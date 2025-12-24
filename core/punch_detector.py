import numpy as np
import collections

class PunchDetector:
    def __init__(self, model_path=None):
        """
        Initialize PunchDetector.
        :param model_path: Path to the trained Random Forest model (optional).
                           If None, uses heuristic detection.
        """
        self.model = None
        if model_path:
            # self.model = load_model(model_path) # TODO: Implement model loading
            pass

        # History for velocity calculation (last 5 frames)
        self.left_hand_history = collections.deque(maxlen=5)
        self.right_hand_history = collections.deque(maxlen=5)
        
        # State tracking
        self.left_hand_state = "RETRACTED" # RETRACTED, EXTENDING, RETURNING
        self.right_hand_state = "RETRACTED"
        
        # Hyperparameters (heuristic)
        self.VELOCITY_THRESHOLD = 0.5 # Arbitrary unit, needs calibration

    def process(self, landmarks):
        """
        Process new landmarks to detect punches.
        :param landmarks: List of [id, x, y, z, visibility] from PoseDetector
        :return: List of detected punches e.g., ["Left Jab", "Right Cross"]
        """
        detected_punches = []
        
        if not landmarks:
            return detected_punches

        # MediaPipe Landmark Indices:
        # 15: Left Wrist, 16: Right Wrist
        # 11: Left Shoulder, 12: Right Shoulder
        
        # Extract features
        left_wrist = self._get_landmark_pos(landmarks, 15)
        right_wrist = self._get_landmark_pos(landmarks, 16)
        
        # Update history
        self.left_hand_history.append(left_wrist)
        self.right_hand_history.append(right_wrist)
        
        # Calculate velocity if we have enough history
        if len(self.left_hand_history) >= 2:
            left_vel = self._calculate_velocity(self.left_hand_history)
            right_vel = self._calculate_velocity(self.right_hand_history)
            
            # Simple Heuristic Detection (Placeholder for ML)
            punch = self._detect_heuristic(left_vel, right_vel, landmarks)
            if punch:
                detected_punches.append(punch)
                
        return detected_punches

    def _get_landmark_pos(self, landmarks, id):
        for lm in landmarks:
            if lm[0] == id:
                return np.array([lm[1], lm[2]]) # x, y
        return np.array([0, 0])

    def _calculate_velocity(self, history):
        # Simple displacement between last two frames
        p1 = history[-1]
        p2 = history[-2]
        return np.linalg.norm(p1 - p2)

    def _detect_heuristic(self, left_vel, right_vel, landmarks):
        # Very basic state machine
        # TODO: Improve with real mechanics (extension checks, retract checks)
        
        # Check Left Punch
        if left_vel > 20: # Threshold in pixels (approx)
            if self.left_hand_state == "RETRACTED":
                self.left_hand_state = "EXTENDING"
                return "Left Jab" # Assuming lead hand is left for now
        elif left_vel < 5:
             self.left_hand_state = "RETRACTED"

        # Check Right Punch
        if right_vel > 20: 
            if self.right_hand_state == "RETRACTED":
                self.right_hand_state = "EXTENDING"
                return "Right Cross"
        elif right_vel < 5:
            self.right_hand_state = "RETRACTED"
            
        return None
