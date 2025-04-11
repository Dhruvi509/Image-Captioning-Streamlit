import streamlit as st
import os
import uuid
import time
from PIL import Image
from main import detect_objects, generate_caption, translate_text, text_to_speech

# Folder setup
UPLOAD_FOLDER = "temp_uploads"
AUDIO_FOLDER = "temp_audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Language mapping: Full name -> Language code
language_options = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Telugu": "te",
    "Bengali": "bn",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "Italian": "it",
    "Russian": "ru"
}

# Streamlit UI
st.set_page_config(page_title="Echo Vision", layout="centered")
st.title("🔊 Echo Vision")
st.write("Upload an image to get AI-generated captions, object detection, translations, and audio output.")

# Upload & language selection
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
language_name = st.selectbox("Select output language", list(language_options.keys()))
language = language_options[language_name]

if uploaded_file:
    # Clear old files
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    for f in os.listdir(AUDIO_FOLDER):
        os.remove(os.path.join(AUDIO_FOLDER, f))

    # Save uploaded image
    img_id = str(uuid.uuid4())
    img_filename = f"{img_id}.jpg"
    img_path = os.path.join(UPLOAD_FOLDER, img_filename)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.read())

    # Display image
    st.image(Image.open(img_path), caption="Uploaded Image", use_container_width=True)

    # Processing
    with st.spinner("🔍 Detecting objects..."):
        objects = detect_objects(img_path)

    with st.spinner("📝 Generating caption..."):
        caption = generate_caption(img_path)

    with st.spinner("🌐 Translating..."):
        translated_caption = translate_text(caption, language)

    with st.spinner("🎧 Generating audio..."):
        audio_filename = f"{img_id}_{language}.mp3"
        audio_path = text_to_speech(translated_caption, language, audio_filename)
        time.sleep(0.5)

    # Results
    st.success("✅ Done!")
    st.markdown(f"**🧩 Objects Detected:** {', '.join(objects) if objects else 'No objects detected.'}")
    st.markdown(f"**📝 Caption:** {caption}")
    st.markdown(f"**🌍 Translated ({language_name}):** {translated_caption}")

    if audio_path and os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mpeg")
