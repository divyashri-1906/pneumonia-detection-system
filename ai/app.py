from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained AI model
model = tf.keras.models.load_model("pneumonia_model.keras")


@app.get("/")
def home():
    return {"message": "Pneumonia AI API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    image_data = await file.read()

    # Convert image to PIL image
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Resize image
    image = image.resize((224, 224))

    # Convert image to array
    image_array = np.array(image) / 255.0

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # AI prediction
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