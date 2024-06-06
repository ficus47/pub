import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import numpy as np
import os
from PIL import Image
from moviepy.editor import ImageSequenceClip

class VideoRecorder(VideoProcessorBase):
    def __init__(self):
        self.frames = []
        self.recording = False

    def recv(self, frame):
        img = frame.to_image()
        if self.recording:
            self.frames.append(np.array(img))
            if len(self.frames) / 30 > 5:  # Assuming 30 fps
                self.stop_recording()

    def stop_recording(self):
        self.recording = False

        # Convert frames to video using moviepy
        clip = ImageSequenceClip(self.frames, fps=30)
        clip.write_videofile("recorded_video.mp4", codec='libx264')

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

    if os.path.isfile("recorded_video.mp4"):
        st.video("recorded_video.mp4")

if __name__ == "__main__":
    main()
