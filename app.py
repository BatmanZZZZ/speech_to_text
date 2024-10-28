import streamlit as st
import wave
import uuid
from speech_to_text import SpeechToText
from audio_recorder_streamlit import audio_recorder

st.title("Speech to Refine Prompt")

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "speech_to_text" not in st.session_state:
    st.session_state.speech_to_text = SpeechToText()

# Function to save the audio file
def save_audio_file(audio_data):
    audio_file_path = "audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_data)
    return audio_file_path

# Display transcribed text in the center of the page
def display_transcribed_text(transcribed_text):
    st.session_state.messages.append({"role": "user", "content": transcribed_text})

# Audio recording
audio_data = audio_recorder()

if audio_data is not None:
    audio_file_path = save_audio_file(audio_data)
    with st.spinner("Thinking..."):
        try:
            transcribed_text = st.session_state.speech_to_text.get_refined_trancribed_text(audio_file_path)
            display_transcribed_text(transcribed_text)
        except Exception as e:
            st.error(f"Error: {e}")

# Render the chat messages in the middle of the page (AFTER the column layout)
for message in st.session_state.messages:
    st.markdown(f"<h3 style='text-align: center;'>{message['content']}</h3>", unsafe_allow_html=True)