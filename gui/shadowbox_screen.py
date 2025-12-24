import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from core.pose_detector import PoseDetector
from core.punch_detector import PunchDetector
from core.metrics_calculator import MetricsCalculator

class ShadowboxScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Shadowboxing Analysis")
        self.geometry("1200x800")
        self.configure(bg="#34495e")
        
        # Core Logic
        self.running = False
        self.cap = None
        self.detector = PoseDetector()
        self.punch_detector = PunchDetector()
        self.metrics = MetricsCalculator()

        self.create_widgets()

    def create_widgets(self):
        # Top Control Bar
        control_frame = tk.Frame(self, bg="#2c3e50", padx=10, pady=10)
        control_frame.pack(side="top", fill="x")
        
        self.btn_start = ttk.Button(control_frame, text="Start Camera", command=self.toggle_camera)
        self.btn_start.pack(side="left", padx=5)
        
        btn_back = ttk.Button(control_frame, text="Back to Menu", command=self.destroy)
        btn_back.pack(side="right", padx=5)

        # Main Layout: Video Left, Stats Right
        content_frame = tk.Frame(self, bg="#34495e")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Video Canvas
        self.video_label = tk.Label(content_frame, bg="black")
        self.video_label.pack(side="left", fill="both", expand=True)

        # Stats Panel
        stats_frame = tk.Frame(content_frame, bg="#2c3e50", width=300)
        stats_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # Stats Labels
        tk.Label(stats_frame, text="Statistics", font=("Helvetica", 18, "bold"), 
                 bg="#2c3e50", fg="white").pack(pady=20)
        
        self.lbl_total = self.create_stat_label(stats_frame, "Total Strikes: 0")
        self.lbl_jabs = self.create_stat_label(stats_frame, "Jabs: 0")
        self.lbl_crosses = self.create_stat_label(stats_frame, "Crosses: 0")
        self.lbl_hooks = self.create_stat_label(stats_frame, "Hooks: 0")
        self.lbl_uppercuts = self.create_stat_label(stats_frame, "Uppercuts: 0")

    def create_stat_label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Helvetica", 14), 
                       bg="#2c3e50", fg="#ecf0f1", anchor="w")
        lbl.pack(fill="x", padx=20, pady=10)
        return lbl

    def toggle_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0) # Default camera
            if not self.cap.isOpened():
                print("Error: Could not open camera")
                return
            self.running = True
            self.btn_start.configure(text="Stop Camera")
            self.update_frame()
        else:
            self.running = False
            self.btn_start.configure(text="Start Camera")
            if self.cap:
                self.cap.release()

    def update_frame(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # 1. Pose Detection
                frame = self.detector.find_pose(frame)
                landmarks = self.detector.get_position(frame, draw=False)
                
                # 2. Punch Detection
                punches = self.punch_detector.process(landmarks)
                
                # 3. Metrics Update
                if punches:
                    self.metrics.update_punches(punches)
                    self.update_stats_display()
                    # Visual feedback on frame
                    cv2.putText(frame, f"PUNCH: {punches[-1]}", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Convert to ImageTk
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                # Resize to fit (optional)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_label.imgtk = imgtk # Keep reference
                self.video_label.configure(image=imgtk)
            
            self.after(10, self.update_frame)

    def update_stats_display(self):
        stats = self.metrics.get_stats()
        self.lbl_total.configure(text=f"Total Strikes: {stats['total_strikes']}")
        self.lbl_jabs.configure(text=f"Jabs: {stats['jabs']}")
        self.lbl_crosses.configure(text=f"Crosses: {stats['crosses']}")
        self.lbl_hooks.configure(text=f"Hooks: {stats['hooks']}")
        self.lbl_uppercuts.configure(text=f"Uppercuts: {stats['uppercuts']}")

    def destroy(self):
        self.running = False
        if self.cap:
            self.cap.release()
        super().destroy()
