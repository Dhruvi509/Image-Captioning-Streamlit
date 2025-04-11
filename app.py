import streamlit as st
import os
import uuid
import shutil
from PIL import Image
from main import detect_objects, generate_caption, translate_text, text_to_speech

# Temp folders
UPLOAD_FOLDER = "temp_uploads"
AUDIO_FOLDER = "temp_audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Title and description
st.set_page_config(page_title="Echo Vision: Image Captioning App", layout="centered")
st.title("🧠 Echo Vision")
st.write("Upload an image, get objects, caption, translation and audio.")

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
language = st.selectbox("Select language", [
    "en", "hi", "es", "fr", "ta", "gu", "te", "bn",
    "kn", "ml", "mr", "pa", "ur", "zh-cn", "ja", "ko", "de", "it", "ru"
])

if uploaded_file:
    # Clean previous uploads
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    for f in os.listdir(AUDIO_FOLDER):
        os.remove(os.path.join(AUDIO_FOLDER, f))

    # Save image
    img_id = str(uuid.uuid4())
    img_filename = f"{img_id}.jpg"
    img_path = os.path.join(UPLOAD_FOLDER, img_filename)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.read())

    # Display image
    st.image(Image.open(img_path), caption="Uploaded Image", use_column_width=True)

    with st.spinner("Detecting objects..."):
        objects = detect_objects(img_path)

    with st.spinner("Generating caption..."):
        caption = generate_caption(img_path)

    with st.spinner("Translating..."):
        translated_caption = translate_text(caption, language)

    with st.spinner("Generating audio..."):
        audio_filename = f"{img_id}_{language}.mp3"
        audio_path = text_to_speech(translated_caption, language, audio_filename)

    # Show results
    st.success("✅ Done!")
    st.markdown(f"**🧩 Objects Detected:** {', '.join(objects)}")
    st.markdown(f"**📝 Caption:** {caption}")
    st.markdown(f"**🌍 Translated ({language}):** {translated_caption}")
    
    if audio_path and os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mp3")
