import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

# Image settings
IMAGE_SIZE = 224
BATCH_SIZE = 32

# Dataset paths
train_path = "../chest_xray/chest_xray/train"
val_path = "../chest_xray/chest_xray/val"

# Prepare training images
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

# Prepare validation images
val_datagen = ImageDataGenerator(
    rescale=1.0 / 255
)

# Load training dataset
train_data = train_datagen.flow_from_directory(
    train_path,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

# Load validation dataset
val_data = val_datagen.flow_from_directory(
    val_path,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

# Create CNN model
model = models.Sequential([
    layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3)),

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),

    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),

    layers.Dense(1, activation="sigmoid")
])

# Configure model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Display model information
model.summary()

# Train the model
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

# Save trained model
model.save("pneumonia_model.keras")

print("Training completed successfully!")
print("Model saved as pneumonia_model.keras")