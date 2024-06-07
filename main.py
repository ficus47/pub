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

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frames = []
        self.start_time = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if self.start_time is None:
            self.start_time = time.time()

        if time.time() - self.start_time < 5:
            self.frames.append(img)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Configurer le streamer
ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if ctx.video_transformer:
    # Sauvegarder les images après 5 secondes
    if time.time() - ctx.video_transformer.start_time > 5 and ctx.video_transformer.frames:
        for i, frame in enumerate(ctx.video_transformer.frames):
            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            Image.fromarray(frame).save(frame_path)
        st.write("Images capturées et sauvegardées.")

        # Assembler les images en vidéo
        clip = ImageSequenceClip(output_dir, fps=10)
        clip.write_videofile("output_video.mp4")
        st.write("Vidéo créée : output_video.mp4")
        ctx.video_transformer.frames = []  # Réinitialiser les frames après la création de la vidéo


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
    height=600,  # Ajustez la hauteur si nécessaire
)

st.write("**bonjour**")