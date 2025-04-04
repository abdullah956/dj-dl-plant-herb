import os
import json
import numpy as np
import cv2
import tensorflow as tf
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from tensorflow.keras.models import load_model
from .models import ContactMessage, NewsletterSubscriber

model = load_model(os.path.join(settings.BASE_DIR, 'work', 'plant_work', 'plant.h5'))

class_names_file_path = os.path.join(settings.BASE_DIR, 'work', 'plant_work', 'plant_class.json')
with open(class_names_file_path, 'r') as file:
    CLASS_NAMES = json.load(file)

cause_file_path = os.path.join(settings.BASE_DIR, 'work', 'plant_work', 'plant_cause.json')
with open(cause_file_path, 'r') as file:
    CAUSE_NAMES = json.load(file)

qualities_file_path = os.path.join(settings.BASE_DIR, 'work', 'plant_work', 'plant_qualities.json')
with open(qualities_file_path, 'r') as file:
    QUALITY_NAMES = json.load(file)

def extract_name(image_name):
    return " ".join(image_name.split()[:-1])

def predict_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_name = os.path.splitext(image.name)[0]
        extracted_name = extract_name(image_name)

        plant_data = CAUSE_NAMES
        qualities_data = QUALITY_NAMES

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
    sent = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        sent = True
        messages.success(request, "Your message has been sent. Thank you!")
        return redirect("contact")

    return render(request, "contact.html", {"sent": sent})

def predict_by_model_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        full_path = default_storage.path(file_path)

        img = cv2.imread(full_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img)
        class_idx = np.argmax(prediction)
        predicted_class = CLASS_NAMES[class_idx]

        return render(request, "plant/predict.html", {"predicted_class": predicted_class})

    return render(request, "plant/predict.html")


def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not NewsletterSubscriber.objects.filter(email=email).exists():
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, "Your subscription request has been sent. Thank you!")
        else:
            messages.warning(request, "You are already subscribed.")

        return redirect("home")
