import os
import random
import string

DATASET_PATH = r"C:\Users\PMLS\Desktop\Projects\data science\dj-dl-plant\PlantDoc-Dataset"

def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

for folder in ["train", "test"]:
    folder_path = os.path.join(DATASET_PATH, folder)
    for class_folder in os.listdir(folder_path):
        class_path = os.path.join(folder_path, class_folder)
        if os.path.isdir(class_path):
            for filename in os.listdir(class_path):
                old_path = os.path.join(class_path, filename)
                if os.path.isfile(old_path):
                    ext = os.path.splitext(filename)[1]  # Keep original extension
                    new_name = generate_random_name() + ext
                    new_path = os.path.join(class_path, new_name)
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
