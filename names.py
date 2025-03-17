import os

def rename_images(dataset_path):
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if os.path.isdir(class_path):
            images = sorted(os.listdir(class_path))  # Get all images in sorted order
            for index, image in enumerate(images):
                ext = os.path.splitext(image)[-1]  # Get file extension
                new_name = f"{class_folder} {index}{ext}"
                old_path = os.path.join(class_path, image)
                new_path = os.path.join(class_path, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

dataset_path = r"PlantDoc-Dataset\test"  # Change to your dataset folder
rename_images(dataset_path)
