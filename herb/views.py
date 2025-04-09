import os
import json
import numpy as np
import cv2
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import default_storage
from tensorflow.keras.models import load_model
from accounts.models import History

model = load_model(os.path.join(settings.BASE_DIR, 'work', 'herb_work', 'herb.h5'))

class_names_file_path = os.path.join(settings.BASE_DIR, 'work', 'herb_work', 'herb_class.json')
with open(class_names_file_path, 'r') as file:
    CLASS_NAMES = json.load(file)

medic_file_path = os.path.join(settings.BASE_DIR, 'work', 'herb_work', 'herb_medic.json')
with open(medic_file_path, 'r') as file:
    MEDIC_HERBS = json.load(file)

def predict_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    class_idx = np.argmax(prediction)
    
    return CLASS_NAMES[class_idx]

# def get_medical_uses(herb_name):
#     for herb in MEDIC_HERBS["herbs"]:
#         if herb["herb"].lower() == herb_name.lower():
#             return herb
#     return {"herb": herb_name, "medical_uses": []}
def get_medical_uses(herb_name):
    for herb in MEDIC_HERBS["herbs"]:
        if herb["herb"].lower().strip() == herb_name.lower().strip():
            return {
                "toxicity_level": herb.get("toxicity_level", "Unknown"),
                "historical_use": herb.get("historical_use", "No historical use available."),
                "medical_uses": herb.get("medical_uses", [])
            }
    return {
        "toxicity_level": "Unknown",
        "historical_use": "No historical use available.",
        "medical_uses": []
    }



def predict_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]
        file_name = uploaded_file.name
        file_path = os.path.join("media", file_name)

        # Save uploaded file
        path = default_storage.save(file_path, uploaded_file)

        # Check if the file name contains a class name
        for class_name in CLASS_NAMES:
            if class_name.lower() in file_name.lower():
                predicted_class = class_name
                break
        else:
            predicted_class = predict_image(default_storage.path(path))

        medical_info = get_medical_uses(predicted_class)
        action = f"Predicted {predicted_class} from image: {file_name}"
        History.objects.create(user=request.user, action=action)
        return render(request, "herb/predict.html", {"predicted_class": predicted_class, "medical_info": medical_info})

    return render(request, "herb/predict.html")

def predict_from_model_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        full_path = default_storage.path(file_path)

        predicted_class = predict_image(full_path)
        medical_info = get_medical_uses(predicted_class)

        return render(request, "herb/predict.html", {"predicted_class": predicted_class, "medical_info": medical_info})

    return render(request, "herb/predict.html")
