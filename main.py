import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import cv2
import numpy as np
import os

class VideoRecorder(VideoProcessorBase):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []
        self.stop_recording = False

    def recv(self, frame):
        if not self.stop_recording:
            self.frames.append(frame.to_ndarray(format="bgr24"))

def save_video(frames, filename="video.mp4"):
    frame_height, frame_width, _ = frames[0].shape
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (frame_width, frame_height))
    for frame in frames:
        out.write(frame)
    out.release()

def main():
    st.title("Video Recorder with Streamlit-WebRTC")

    recorder = VideoRecorder()

    client_settings = ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    )

    webrtc_ctx = webrtc_streamer(
        key="example",
        client_settings=client_settings,
        video_processor_factory=VideoRecorder,
    )

    if webrtc_ctx.video_processor:
        st.write("Recording...")
        if st.button("Stop Recording"):
            webrtc_ctx.video_processor.stop_recording = True

    if hasattr(webrtc_ctx, "video_processor") and webrtc_ctx.video_processor.stop_recording:
        st.write("Stopped Recording")
        save_video(webrtc_ctx.video_processor.frames)
        st.video(webrtc_ctx.video_processor.frames)

if __name__ == "__main__":
    main()
