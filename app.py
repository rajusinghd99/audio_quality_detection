import streamlit as st
import soundfile as sf
import numpy as np
from speechmos.aecmos import run as aecmos_run

st.set_page_config(page_title="Audio Quality Evaluator", layout="centered")
st.title("🎧 Audio Quality Evaluator")

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file is not None:
    try:
        audio_data, sample_rate = sf.read(uploaded_file)

        if audio_data.ndim > 1:
            st.warning("Stereo audio detected. Converting to mono.")
            audio_data = np.mean(audio_data, axis=1)

        st.audio(uploaded_file, format="audio/wav")

        # score = aecmos_run(audio_data, sample_rate)
        score = aecmos_run(audio_data, sample_rate, talk_type="far")
        scaled_score = round(score * 2, 2)

        st.success(f"Estimated Audio Quality Score: {scaled_score} / 10")

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
