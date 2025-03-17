import os
import random
import shutil
from glob import glob

# Set dataset path
dataset_path = "Chinese-Herbs-Dataset"

def balance_classes(dataset_path):
    class_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    
    # Get the minimum number of images across all classes
    min_count = min(len(os.listdir(os.path.join(dataset_path, d))) for d in class_dirs)
    
    for class_dir in class_dirs:
        class_path = os.path.join(dataset_path, class_dir)
        images = glob(os.path.join(class_path, "*"))
        random.shuffle(images)
        
        # Keep only min_count images
        for img in images[min_count:]:
            os.remove(img)

def rename_images(dataset_path):
    for class_dir in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_dir)
        if os.path.isdir(class_path):
            images = glob(os.path.join(class_path, "*"))
            random.shuffle(images)
            
            for i, img in enumerate(images):
                ext = os.path.splitext(img)[-1]
                new_name = os.path.join(class_path, f"{class_dir}_{i}{ext}")
                shutil.move(img, new_name)

if __name__ == "__main__":
    balance_classes(dataset_path)
    rename_images(dataset_path)
    print("Dataset balanced and images renamed successfully.")