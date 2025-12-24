class MetricsCalculator:
    def __init__(self):
        self.stats = {
            "left_punches": 0,
            "right_punches": 0,
            "jabs": 0,
            "crosses": 0,
            "hooks": 0,
            "uppercuts": 0,
            "total_strikes": 0,
            "head_coverage_percent": 0.0,
            "footwork_active_percent": 0.0
        }
        self.frame_count = 0
        self.head_covered_frames = 0
        self.active_footwork_frames = 0

    def update_punches(self, punch_types):
        """
        Update punch counts based on detected punches.
        :param punch_types: List of strings e.g. ["Left Jab"]
        """
        for punch in punch_types:
            self.stats["total_strikes"] += 1
            
            if "Left" in punch:
                self.stats["left_punches"] += 1
            if "Right" in punch:
                self.stats["right_punches"] += 1
                
            if "Jab" in punch:
                self.stats["jabs"] += 1
            elif "Cross" in punch:
                self.stats["crosses"] += 1
            elif "Hook" in punch:
                self.stats["hooks"] += 1
            elif "Uppercut" in punch:
                self.stats["uppercuts"] += 1

    def update_defense(self, landmarks):
        """
        Check valid defense (hands near head).
        """
        self.frame_count += 1
        # TODO: Implement geometry check (wrist y < nose y, distance to head small)
        # For now, placeholder
        is_covered = False
        if is_covered:
            self.head_covered_frames += 1
            
        if self.frame_count > 0:
            self.stats["head_coverage_percent"] = (self.head_covered_frames / self.frame_count) * 100

    def get_stats(self):
        return self.stats

    def reset(self):
        self.__init__()
