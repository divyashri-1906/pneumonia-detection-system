import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# Load trained model
model = tf.keras.models.load_model("pneumonia_model.keras")

# Change this to your X-ray image path
image_path = "test_image.jpeg"

# Load and prepare image
image = load_img(image_path, target_size=(224, 224))
image_array = img_to_array(image)
image_array = image_array / 255.0
image_array = np.expand_dims(image_array, axis=0)

# Predict
prediction = model.predict(image_array)[0][0]

# Display result
if prediction >= 0.5:
    print("Prediction: PNEUMONIA")
else:
    print("Prediction: NORMAL")

print("Confidence:", round(float(prediction) * 100, 2), "%")