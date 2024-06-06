import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import cv2
import numpy as np
import os

class VideoRecorder(VideoProcessorBase):
    def __init__(self):
        self.frames = []
        self.recording = False

    def recv(self, frame):
        if self.recording:
            self.frames.append(frame)
            if len(self.frames) * frame.time_stamp > 5:
                self.stop_recording()

    def stop_recording(self):
        self.recording = False

        # Convert frames to video
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        height, width = self.frames[0].shape[:2]
        out = cv2.VideoWriter("recorded_video.mp4", fourcc, 30.0, (width, height))
        for frame in self.frames:
            out.write(cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR))
        out.release()

        st.write("L'enregistrement est terminé. La vidéo a été enregistrée sous recorded_video.mp4.")
        self.close()

def main():
    st.title("Enregistrement Vidéo de 5 Secondes")

    st.write("Appuyez sur le bouton 'Enregistrer' pour démarrer l'enregistrement.")

    webrtc_ctx = webrtc_streamer(
        key="video-recorder",
        video_processor_factory=VideoRecorder,
        client_settings=ClientSettings(
            media_stream_constraints={"video": True, "audio": False},
        ),
    )

    if webrtc_ctx.video_processor:
        if st.button("Enregistrer"):
            webrtc_ctx.video_processor.recording = True
            st.write("L'enregistrement a commencé...")

if __name__ == "__main__":
    main()
    st.video("recorded_video.mp4")if os.isfile("recorded_video.mp4")else ""
