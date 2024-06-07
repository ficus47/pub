import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import os
import time
from moviepy.editor import ImageSequenceClip
import streamlit.components.v1 as components


# Dossier pour sauvegarder les images
output_dir = "captured_frames"
os.makedirs(output_dir, exist_ok=True)

captured_frames = []
is_recording = False

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frames = []
    
    def recv(self, frame):
        if is_recording:
            self.frames.append(frame.to_image())
        return av.VideoFrame.from_image(frame.to_image())

def start_recording():
    global is_recording
    is_recording = True
    st.session_state.video_processor.frames = []

def stop_recording():
    global is_recording
    is_recording = False
    captured_frames.extend(st.session_state.video_processor.frames)

def save_images(frames):
    for i, frame in enumerate(frames):
        frame.save(f'frame_{i}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')

st.title("Streamlit WebRTC Example")

webrtc_ctx = webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)

if webrtc_ctx.video_processor:
    st.session_state.video_processor = webrtc_ctx.video_processor

    if st.button("Start Recording"):
        start_recording()
        st.write("Recording started...")
        threading.Timer(5, stop_recording).start()

    if st.button("Stop and Save Recording"):
        stop_recording()
        save_images(captured_frames)
        st.write("Recording stopped and saved.")

st.write("Captured frames: ", len(captured_frames))

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