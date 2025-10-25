import cv2
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import numpy as np

def show_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # ---- TRUE WIDE VIEW (Zoom Out) ----
        zoom_factor = 0.99  # <1 = zoom out, >1 = zoom in

        # Create a black background same as webcam size
        background = np.zeros_like(frame)

        # Shrink the original frame to make it look wide
        new_w, new_h = int(w * zoom_factor), int(h * zoom_factor)
        small_frame = cv2.resize(frame, (new_w, new_h))

        # Calculate centered placement
        x_offset = (w - new_w) // 2
        y_offset = (h - new_h) // 2

        # Paste smaller frame into center of background
        background[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = small_frame

        frame = background
        frame = cv2.resize(frame, (window_width, window_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    label.after(10, show_camera)

# ---- Setup ----
cap = cv2.VideoCapture(0)
root = tk.Tk()
root.title("Camera Pop-out")

# ---- Position (Bottom-right) ----
screen_width, screen_height = pyautogui.size()
window_width, window_height = 450, 320
x = screen_width - window_width - 30
y = screen_height - window_height - 80
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.attributes("-topmost", True)
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "black")

label = tk.Label(root, bg="black")
label.pack(fill="both", expand=True)

show_camera()
root.mainloop()
cap.release()
