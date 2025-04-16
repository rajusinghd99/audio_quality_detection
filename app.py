import streamlit as st
import soundfile as sf
import numpy as np
from speechmos import aecmos

st.set_page_config(page_title="Audio Quality Evaluator", layout="centered")
st.title("🎧 Audio Quality Evaluator")
st.markdown("Upload a mono or stereo WAV file to assess its quality using the AECMOS model.")

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file is not None:
    try:
        audio_data, sample_rate = sf.read(uploaded_file)

        # Convert stereo to mono if needed
        if audio_data.ndim > 1:
            st.warning("Stereo audio detected. Converting to mono.")
            audio_data = np.mean(audio_data, axis=1)

        # Audio player
        st.audio(uploaded_file, format="audio/wav")


        # Prepare input data as a dictionary inside a list
        input_data = [{
            "wav": audio_data,
            "talk_type": "far"
        }]

        # Run AECMOS model with the correct sample rate passed as a separate argument
        result = aecmos.run(input_data, sr=sample_rate)

        # Extract the MOS score and scale it to 1-10
        score = result[0]["mos"]
        scaled_score = round(score * 2, 2)  # Scale 1–5 to 1–10

        # Display score
        st.success(f"Estimated Audio Quality Score: {scaled_score} / 10")

        # Feedback
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
