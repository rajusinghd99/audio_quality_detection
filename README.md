## 🎧 Audio Quality Evaluator

A simple and interactive Streamlit web application that allows users to upload an audio recording (WAV format) and evaluate its quality using a machine learning model. The app uses the `speechmos` package to calculate a Mean Opinion Score (MOS), providing a score scaled from **1 to 10**.

### 🌟 Features

- 📂 Upload mono or stereo WAV files
- 🎚️ Automatically converts stereo to mono if needed
- 🧠 Uses `aecmos` model from the `speechmos` package for evaluation
- 🔢 Provides a quality score between 1 (poor) and 10 (excellent)
- 🧾 Qualitative feedback on the audio quality
- 🎛️ Easy-to-use Streamlit interface

### 🛠️ Tech Stack

- Python
- Streamlit
- speechmos
- numpy
- soundfile

### 🚀 Live Demo

You can try the live app here: [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

*(Replace with your actual deployed URL)*

### 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/audio-quality-evaluator.git
cd audio-quality-evaluator
pip install -r requirements.txt
streamlit run app.py
```

### 📁 File Structure

```
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
└── README.md            # Project description
```

### 💡 Future Enhancements

- Support additional MOS models (`dnsmos`, `plcmos`)
- Upload multiple files for batch evaluation
- Visualization of audio waveform and spectrogram
- Export results as CSV
