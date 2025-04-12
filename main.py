import torch
import numpy as np
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from ultralytics import YOLO
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
from urllib.request import urlretrieve

# Auto-download YOLOv8 if not found
if not os.path.exists("yolov8n.pt"):
    urlretrieve("https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt", "yolov8n.pt")

# Load models once
yolo_model = YOLO("yolov8n.pt")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def detect_objects(image_path):
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)  # YOLO expects NumPy arrays
    results = yolo_model(image_np)
    detected_objects = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            label = result.names[class_id]
            detected_objects.append(label)
    return list(set(detected_objects))
    
def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        output = caption_model.generate(**inputs)
    caption = processor.batch_decode(output, skip_special_tokens=True)[0]
    return caption

def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def text_to_speech(text, lang_code, filename):
    try:
        supported_langs = [
            'en', 'hi', 'es', 'fr', 'ta', 'gu', 'te', 'bn',
            'kn', 'ml', 'mr', 'pa', 'ur', 'zh-cn', 'ja', 'ko', 'de', 'it', 'ru'
        ]
        if lang_code.lower() not in supported_langs:
            lang_code = 'en'
        tts = gTTS(text=text, lang=lang_code)
        audio_path = os.path.join("temp_audio", filename)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"TTS error: {e}")
        return None
