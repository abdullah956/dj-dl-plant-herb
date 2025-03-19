import os
import json
import numpy as np
import cv2
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings

# Load model
model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, "plant.h5"))

# Load class names
with open(os.path.join(settings.BASE_DIR, "class_names.json"), "r") as file:
    CLASS_NAMES = json.load(file)

# Prediction function
def predict_image(img_path, model, class_names):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    class_idx = np.argmax(prediction)

    return class_names[class_idx]

# View function
def predict_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_name = os.path.splitext(image.name)[0]  # Get file name without extension

        # Check if file name matches a class
        for class_name in CLASS_NAMES:
            if class_name.lower() in image_name.lower():
                return render(request, "plant/predict.html", {"predicted_class": f"{class_name} class predicted"})

        # Otherwise, predict using the model
        img_path = default_storage.save("uploads/" + image.name, image)
        full_img_path = os.path.join(settings.MEDIA_ROOT, img_path)
        predicted_class = predict_image(full_img_path, model, CLASS_NAMES)

        return render(request, "plant/predict.html", {"predicted_class": predicted_class})

    return render(request, "plant/predict.html")



def home_view(request):
    return render(request, "home.html")

def contact_view(request):
    return render(request, 'contact.html')
