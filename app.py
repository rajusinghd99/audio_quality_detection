import streamlit as st
import soundfile as sf
import numpy as np
from speechmos import aecmos

# Page setup
st.set_page_config(page_title="Audio Quality Evaluator", layout="centered")
st.title("🎧 Audio Quality Evaluator")
st.markdown("Upload a WAV file to evaluate its speech quality using the AECMOS model.")

# File upload
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file is not None:
    try:
        # Read the audio and sample rate
        audio_data, sample_rate = sf.read(uploaded_file)

        # Convert stereo to mono
        if audio_data.ndim > 1:
            st.warning("Stereo audio detected. Converting to mono.")
            audio_data = np.mean(audio_data, axis=1)

        st.audio(uploaded_file, format="audio/wav")

        # Handle 48kHz specific requirement for talk_type
        if sample_rate == 48000:
            st.info("48kHz audio detected. Please select a talk type (required for this model).")
            talk_type = st.selectbox("Talk type", ["st", "nst",  "dt"], index=1)
        else:
            talk_type = "dt"  # default for non-48kHz, though model is best for 48kHz

        if st.button("Evaluate Audio Quality"):
            with st.spinner("Evaluating..."):
                # Prepare input sample
                sample_list = [{"wav": audio_data}]
                
                # Run AECMOS model
                result = aecmos.run(sample_list, sr=sample_rate, talk_type=talk_type, verbose=False)

                # Get score and scale to 1–10
                mos_score = result[0]["mos"]
                scaled_score = round(mos_score * 2, 2)

                st.success(f"Estimated Audio Quality Score: {scaled_score} / 10")

                if scaled_score >= 8:
                    st.markdown("✅ **Excellent** quality.")
                elif scaled_score >= 6:
                    st.markdown("👍 **Good** quality.")
                elif scaled_score >= 4:
                    st.markdown("⚠️ **Fair** quality.")
                else:
                    st.markdown("❌ **Poor** quality.")

    except Exception as e:
        st.error(f"An error occurred while processing the audio: {e}")
