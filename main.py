import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return av.VideoFrame.from_ndarray(gray, format="gray")

st.title("Grayscale Video Stream")
webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
