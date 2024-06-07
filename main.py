import streamlit as st
import imageio
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings

class VideoRecorder(VideoProcessorBase):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []

    def recv(self, frame):
        self.frames.append(frame.to_ndarray(format="bgr24"))

def main():
    st.title("Enregistreur vidéo avec Streamlit-WebRTC")

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
        st.write("Enregistrement...")
        if st.button("Arrêter l'enregistrement"):
            webrtc_ctx.video_processor.stop_recording = True

    if hasattr(webrtc_ctx, "video_processor") and webrtc_ctx.video_processor.stop_recording:
        st.write("Arrêt de l'enregistrement")
        st.write("Enregistrement de la vidéo...")
        with st.spinner("Enregistrement de la vidéo..."):
            # Convertir les images en vidéo
            writer = imageio.get_writer("video.mp4", fps=24)
            for frame in recorder.frames:
                writer.append_data(frame)
            writer.close()
        st.success("Vidéo enregistrée avec succès!")

if __name__ == "__main__":
    main()
    try:
        st.video("video.mp4")
    except Exception as e:
        st.write(e)
