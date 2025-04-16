import streamlit as st
import soundfile as sf
import numpy as np
from speechmos import aecmos

st.set_page_config(page_title="Audio Quality Evaluator", layout="centered")
st.title("🎧 Audio Quality Evaluator")
st.markdown("Upload a mono WAV audio file to assess its quality.")

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file is not None:
    try:
        # Read the uploaded audio file
        audio_data, sample_rate = sf.read(uploaded_file)
        
        # Ensure the audio is mono
        if audio_data.ndim > 1:
            st.warning("Stereo audio detected. Converting to mono.")
            audio_data = np.mean(audio_data, axis=1)
        
        # Display audio player
        st.audio(uploaded_file, format='audio/wav')
        
        # Evaluate audio quality using AECMOS
        score = aecmos(audio_data, sample_rate)
        scaled_score = round(score * 2, 2)  # Scale from 1-5 to 1-10
        
        st.success(f"Estimated Audio Quality Score: {scaled_score} / 10")
        
        # Provide qualitative feedback
        if scaled_score >= 8:
            st.markdown("✅ Excellent quality.")
        elif scaled_score >= 6:
            st.markdown("👍 Good quality.")
        elif scaled_score >= 4:
            st.markdown("⚠️ Fair quality.")
        else:
            st.markdown("❌ Poor quality.")
            
    except Exception as e:
        st.error(f"An error occurred while processing the audio: {e}")
