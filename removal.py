import os
import random

# Dataset path (use raw string to avoid escape sequence issues)
DATASET_PATH = r"C:\Users\PMLS\Desktop\Projects\data science\dj-dl-plant\PlantDoc-Dataset\train"  # Change to test if needed

# Get class-wise image counts
class_counts = {cls: len(os.listdir(os.path.join(DATASET_PATH, cls))) for cls in os.listdir(DATASET_PATH)}
min_class_count = min(class_counts.values())  # Find smallest class size

# Delete extra images
for cls, count in class_counts.items():
    class_path = os.path.join(DATASET_PATH, cls)
    images = os.listdir(class_path)
    
    if count > min_class_count:
        images_to_delete = random.sample(images, count - min_class_count)  # Select extra images randomly
        
        for img in images_to_delete:
            img_path = os.path.join(class_path, img)
            if os.path.exists(img_path):  # Ensure the file exists before deleting
                os.remove(img_path)

print("Dataset balanced. Each class now has", min_class_count, "images.")
