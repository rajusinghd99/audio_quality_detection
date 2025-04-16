import streamlit as st
import soundfile as sf
import numpy as np
from speechmos.aecmos import AECMOSEstimator

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
        
        # Always show talk_type selection
        st.subheader("Audio Configuration")
        talk_type = st.selectbox(
            "Select talk type:",
            ["far", "near", "screen"],
            index=0,
            help="Required for AECMOS evaluation: 'far' (distant speaker), 'near' (close speaker), or 'screen' (content sharing)"
        )
        
        if st.button("Evaluate Audio Quality"):
            # Initialize the AECMOS estimator
            aecmos = AECMOSEstimator()
            
            # Run AECMOS evaluation
            score = aecmos.estimate(
                audio_data, 
                fs=sample_rate,
                talk_type=talk_type
            )
            
            scaled_score = round(score * 2, 2)  # Scale 1-5 to 1-10
            
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
