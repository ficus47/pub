import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time
import queue  # Thread-safe queue for storing frames

# Function to process video frames (replace with your processing logic)
def video_frame_callback(frame):
    # Convert frame to a NumPy array (optional, based on storage strategy)
    frame = frame.to_ndarray(format="bgr24")[:, :, ::-1]  # BGR to RGB (optional)

    # Store frame (array or bytes) in the queue
    video_frames.put(frame) 
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

        # Combine frames into a single byte string for Streamlit
        recorded_video_bytes = b''.join(list(video_frames.queue))

        # (Optional) Display or use the recorded video bytes
        st.video(recorded_video_bytes)  # Assuming Streamlit supports video from bytes

    except queue.Empty:
        # Handle potential timeout if no frames are received
        pass

    # Check for stop condition (e.g., button press, timeout)
    if time.time() - start_time > 3:  # Record for 10 seconds
        is_recording = False
        break
if video_frames:
    st.video(video_frames)
# Process and store the recorded video (if any) elsewhere (optional)
