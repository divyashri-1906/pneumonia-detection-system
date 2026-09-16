from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_download
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download the trained model from Hugging Face
model_path = hf_hub_download(
    repo_id="divya1906/pneumonia-detection-model",
    filename="pneumonia_model.keras"
)

# Load the trained AI model
model = tf.keras.models.load_model(model_path)


@app.get("/")
def home():
    return {"message": "Pneumonia AI API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_data = await file.read()

    image = Image.open(
        io.BytesIO(image_data)
    ).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image) / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    prediction = model.predict(image_array)[0][0]

    if prediction >= 0.5:
        result = "PNEUMONIA"
        confidence = float(prediction) * 100
    else:
        result = "NORMAL"
        confidence = (1 - float(prediction)) * 100

    return {
        "prediction": result,
        "confidence": round(confidence, 2)
    }