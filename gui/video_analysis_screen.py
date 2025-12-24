import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
from core.pose_detector import PoseDetector
from core.punch_detector import PunchDetector
from core.metrics_calculator import MetricsCalculator

class VideoAnalysisScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Video Analysis")
        self.geometry("1200x800")
        self.configure(bg="#34495e")
        
        self.running = False
        self.cap = None
        self.detector = PoseDetector()
        self.punch_detector = PunchDetector()
        self.metrics = MetricsCalculator()
        self.video_path = None

        self.create_widgets()

    def create_widgets(self):
        # Controls
        control_frame = tk.Frame(self, bg="#2c3e50", padx=10, pady=10)
        control_frame.pack(side="top", fill="x")
        
        btn_load = ttk.Button(control_frame, text="Load Video", command=self.load_video)
        btn_load.pack(side="left", padx=5)
        
        self.btn_play = ttk.Button(control_frame, text="Play/Pause", command=self.toggle_play, state="disabled")
        self.btn_play.pack(side="left", padx=5)
        
        btn_back = ttk.Button(control_frame, text="Back to Menu", command=self.destroy)
        btn_back.pack(side="right", padx=5)

        # Content
        content_frame = tk.Frame(self, bg="#34495e")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.video_label = tk.Label(content_frame, bg="black")
        self.video_label.pack(side="left", fill="both", expand=True)

        # Stats
        stats_frame = tk.Frame(content_frame, bg="#2c3e50", width=300)
        stats_frame.pack(side="right", fill="y", padx=(10, 0))
        
        tk.Label(stats_frame, text="Analysis Stats", font=("Helvetica", 18, "bold"), 
                 bg="#2c3e50", fg="white").pack(pady=20)
        
        self.lbl_total = self.create_stat_label(stats_frame, "Total Strikes: 0")
        self.lbl_jabs = self.create_stat_label(stats_frame, "Jabs: 0")
        self.lbl_crosses = self.create_stat_label(stats_frame, "Crosses: 0")
        # Add simpler stats for now

    def create_stat_label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Helvetica", 14), 
                       bg="#2c3e50", fg="#ecf0f1", anchor="w")
        lbl.pack(fill="x", padx=20, pady=10)
        return lbl

    def load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if file_path:
            self.video_path = file_path
            self.cap = cv2.VideoCapture(self.video_path)
            self.btn_play.configure(state="normal")
            # Show first frame
            ret, frame = self.cap.read()
            if ret:
                self.show_frame(frame)

    def toggle_play(self):
        if not self.running:
            if self.cap is None and self.video_path:
                 self.cap = cv2.VideoCapture(self.video_path)
            self.running = True
            self.update_frame()
        else:
            self.running = False

    def update_frame(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Detect and Analyze
                frame = self.detector.find_pose(frame)
                landmarks = self.detector.get_position(frame, draw=False)
                punches = self.punch_detector.process(landmarks)
                
                if punches:
                    self.metrics.update_punches(punches)
                    self.update_stats_display()
                    cv2.putText(frame, f"PUNCH: {punches[-1]}", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                self.show_frame(frame)
                self.after(30, self.update_frame) # Approx 30 FPS
            else:
                self.running = False # End of video
                self.cap.release()
                self.cap = None

    def show_frame(self, frame):
        # Resize for display to fit window if needed
        # For simplicity, just show scaling
        h, w = frame.shape[:2]
        display_h = 600
        scale = display_h / h
        display_w = int(w * scale)
        frame = cv2.resize(frame, (display_w, display_h))
        
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def update_stats_display(self):
        stats = self.metrics.get_stats()
        self.lbl_total.configure(text=f"Total Strikes: {stats['total_strikes']}")
        self.lbl_jabs.configure(text=f"Jabs: {stats['jabs']}")
        self.lbl_crosses.configure(text=f"Crosses: {stats['crosses']}")

    def destroy(self):
        self.running = False
        if self.cap:
            self.cap.release()
        super().destroy()
