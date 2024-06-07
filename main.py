import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import numpy as np

class VideoRecorder(VideoProcessorBase):
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame):
        self.frames.append(frame.to_ndarray(format="bgr24"))

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
        if st.button("Stop Recording"):
            webrtc_ctx.video_processor.stop()
            st.video(recorder.frames)

if __name__ == "__main__":
    main()
