import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import av
import threading
import time
from PIL import Image
import numpy as np
import os
from datetime import datetime, timedelta

# Define the directory to save images
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

# Video transformer class for webrtc_streamer
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frames = []
        self.lock = threading.Lock()
        self.capturing = False
        self.capture_end_time = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        with self.lock:
            if self.capturing:
                self.frames.append(img)
                if datetime.now() >= self.capture_end_time:
                    self.capturing = False
        return frame

    def start_capture(self, duration):
        self.capturing = True
        self.frames = []
        self.capture_end_time = datetime.now() + timedelta(seconds=duration)

# Instantiate the video transformer
video_transformer = VideoTransformer()

# Streamlit UI
st.title("WebRTC Image Capture")
webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if webrtc_ctx.video_transformer:
    if st.button("Start Capture for 5 seconds"):
        video_transformer.start_capture(5)

        while video_transformer.capturing:
            time.sleep(0.1)  # Small sleep to avoid high CPU usage

        with video_transformer.lock:
            captured_frames = video_transformer.frames[:]

        for i, frame in enumerate(captured_frames):
            img = Image.fromarray(frame)
            img.save(os.path.join(save_dir, f"image_{i}.png"))

        st.success(f"Captured {len(captured_frames)} images.")
        st.write(f"Images saved to '{save_dir}'")

