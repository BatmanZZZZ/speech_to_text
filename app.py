import streamlit as st
import wave
import pyaudio
import uuid
from speech_to_text import SpeechToText

st.title("Speech to Refine Prompt")

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "speech_to_text" not in st.session_state:
    st.session_state.speech_to_text = SpeechToText()
if "recording" not in st.session_state:
    st.session_state.recording = False
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = []

# Function to start recording
def start_recording():
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    st.session_state.audio_frames = []

    st.write("Recording... Speak now!")
    
    while st.session_state.recording:
        data = stream.read(chunk)
        st.session_state.audio_frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to save the audio file
def save_audio_file():
    audio_file_path = "audio.wav"
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    # Save the recorded frames to a file
    with wave.open(audio_file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(st.session_state.audio_frames))

    return audio_file_path

# Display transcribed text in the center of the page
def display_transcribed_text(transcribed_text):
    st.session_state.messages.append({"role": "user", "content": transcribed_text})
    # st.markdown(f"<h3 style='text-align: center;'>{transcribed_text}</h3>", unsafe_allow_html=True)

# Create two buttons (Start and Stop) side by side
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Recording"):
        st.session_state.recording = True
        start_recording()

with col2:
    if st.button("Stop Recording"):
        st.session_state.recording = False
        if st.session_state.audio_frames:
            audio_file_path = save_audio_file()

            with st.spinner("Thinking..."):
                try:
                    transcribed_text = st.session_state.speech_to_text.get_refined_trancribed_text(audio_file_path)
                    display_transcribed_text(transcribed_text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("No audio recorded. Please try again.")

# Render the chat messages in the middle of the page (AFTER the column layout)
for message in st.session_state.messages:
    st.markdown(f"<h3 style='text-align: center;'>{message['content']}</h3>", unsafe_allow_html=True)
