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

import streamlit as st
import streamlit_webrtc as webctr
import recorder

st.title("Enregistreur de Vidéo")

# Utiliser Streamlit-WebCTR pour capturer la vidéo
video_data = webctr.video_recorder(
    format="webm",
    video_length=10,  # durée maximale de la vidéo en secondes
    key="video_recorder"
)

if video_data:
    # Afficher un message indiquant que la vidéo a été enregistrée
    st.success("Vidéo enregistrée avec succès!")

    # Afficher la vidéo enregistrée
    st.video(video_data)

    # Préparer la vidéo pour l'envoi au serveur
    # Ici, vous pouvez ajouter le code pour envoyer la vidéo à un serveur
    # en utilisant une requête HTTP par exemple (e.g., avec requests)
    # Ne pas implémenter cela ici comme demandé

else:
    st.warning("Cliquez sur le bouton pour enregistrer une vidéo.")

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