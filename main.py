import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, VideoProcessorBase
import av
import os
import time
from PIL import Image
import datetime
from moviepy.editor import ImageSequenceClip
import streamlit.components.v1 as components
import threading


# Créez un dossier pour stocker les images capturées
output_folder = "captured_images"
os.makedirs(output_folder, exist_ok=True)

# Variables globales pour le contrôle d'enregistrement
is_recording = False

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.lock = threading.Lock()

    def recv(self, frame):
        print("1")
        img = frame.to_image()
        with self.lock:
            if is_recording:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                img.save(os.path.join(output_folder, f"frame_{timestamp}.png"))
        return av.VideoFrame.from_image(img)

def start_recording():
    global is_recording
    is_recording = True

def stop_recording():
    global is_recording
    is_recording = False

st.title("Streamlit WebRTC Image Capture")

webrtc_ctx = webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)

if webrtc_ctx.video_processor:
    if st.button("Start Recording"):
        start_recording()
        st.write("Recording started...")

    if st.button("Stop Recording"):
        stop_recording()
        st.write("Recording stopped.")

st.write(f"Captured frames are saved in the '{output_folder}' folder. file lenght : {len(os.listdir(output_folder))}")

head_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8075907034534804"
     crossorigin="anonymous"></script>
"""

# Utilisez la fonction components.html pour insérer le code dans la page
components.html(
    f"""
    <html>
    <head>
        {head_code}
    </head>
    <body>
        <!-- Le contenu principal de votre application Streamlit -->
        <h1>Bienvenue sur mon site Streamlit</h1>
        <p>Voici un exemple d'application Streamlit avec une publicité Google AdSense.</p>
    </body>
    </html>
    """,
    height=10,  # Ajustez la hauteur si nécessaire
)

st.write("**bonjour**")