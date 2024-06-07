import streamlit as st
import imageio
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings

class VideoRecorder(VideoProcessorBase):
    def __init__(self) -> None:
        super().__init__()
        self.frames = []
        self.stop_recording = False  # Initialize stop_recording attribute to False

    def recv(self, frame):
        if not self.stop_recording:
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

    if recorder.stop_recording:  # Check the stop_recording attribute of the recorder object
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
