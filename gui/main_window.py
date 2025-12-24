import tkinter as tk
from tkinter import ttk
from gui.shadowbox_screen import ShadowboxScreen
from gui.video_analysis_screen import VideoAnalysisScreen

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartStrike2 - Boxing Analysis")
        self.geometry("800x600")
        self.configure(bg="#2c3e50")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 14), padding=10)
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self, text="SmartStrike2", font=("Helvetica", 32, "bold"), 
                          bg="#2c3e50", fg="white")
        header.pack(pady=50)

        # Mode Buttons
        btn_frame = tk.Frame(self, bg="#2c3e50")
        btn_frame.pack(pady=20)

        btn_shadowbox = ttk.Button(btn_frame, text="Shadowboxing Analysis", 
                                   command=self.open_shadowbox)
        btn_shadowbox.pack(pady=10, fill='x')

        btn_sparring = ttk.Button(btn_frame, text="Sparring Analysis (Coming Soon)", 
                                  state="disabled")
        btn_sparring.pack(pady=10, fill='x')
        
        btn_video = ttk.Button(btn_frame, text="Video File Analysis", 
                               command=self.open_video_analysis)
        btn_video.pack(pady=10, fill='x')
        
        btn_exit = ttk.Button(btn_frame, text="Exit", command=self.quit)
        btn_exit.pack(pady=30, fill='x')

    def open_shadowbox(self):
        ShadowboxScreen(self)

    def open_video_analysis(self):
        VideoAnalysisScreen(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
