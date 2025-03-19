import os
import json
import numpy as np
import cv2
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, "plant.h5"))

with open(os.path.join(settings.BASE_DIR, "class_names.json"), "r") as file:
    CLASS_NAMES = json.load(file)

def extract_name(image_name):
    return " ".join(image_name.split()[:-1])

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def predict_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_name = os.path.splitext(image.name)[0]
        extracted_name = extract_name(image_name)

        plant_data = load_json("plant.json")
        qualities_data = load_json("qualities.json")

        if extracted_name in plant_data:
            result = plant_data[extracted_name]
        elif extracted_name in qualities_data:
            result = qualities_data[extracted_name]
        else:
            result = {"message": "No matching data found"}

        return render(request, "plant/predict.html", {"predicted_class": extracted_name, "result": result})

    return render(request, "plant/predict.html")

def home_view(request):
    return render(request, "home.html")

def contact_view(request):
    return render(request, "contact.html")
