import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time
import queue  # Thread-safe queue for storing frames
import moviepy.editor as mpe  # Import moviepy for video creation

# Function to process video frames and store them
def video_frame_callback(frame):
    # Convert frame to a format suitable for storage (e.g., bytes)
    # Example: Convert BGR to RGB and then to JPEG bytes
    frame = frame.to_ndarray(format="bgr24")[:, :, ::-1]  # BGR to RGB
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Store frame bytes in the queue
    video_frames.put(frame_bytes)

# Create an empty queue to store video frames
video_frames = queue.Queue()

# Streamlit video recording component
st.header("Video Recording")

webrtc_streamer(
    key="video-streamer",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},  # Disable audio
)

# Button to initiate recording
record_button = st.button("Record Video")

# Flag to indicate recording state
is_recording = False

if record_button:
    is_recording = True
    start_time = time.time()  # Record start time

# Loop to process recorded frames and stop recording after a duration
while is_recording:
    # Check for new frames in the queue
    try:
        frame_bytes = video_frames.get(timeout=1)  # Wait for a frame for 1 second
        # Update progress bar or display a recording indicator (optional)
    except queue.Empty:
        # Handle potential timeout if no frames are received
        pass

    # Check for stop condition (e.g., button press, timeout)
    if time.time() - start_time > 5:  # Record for 10 seconds
        is_recording = False
        break

if not video_frames.empty():
    # Convert bytes to NumPy array and create clips
    video_clips = [mpe.ImageClip(np.frombuffer(frame_bytes, dtype=np.uint8).reshape((height, width, 3))) for frame_bytes in video_frames]

    # Create and save the final video using concatenate_videoclips
    final_clip = mpe.concatenate_videoclips(video_clips)
    final_clip.write_videofile("recorded_video.mp4", fps=30)