import os
import json

data_dir = "Chinese-Herbs-Dataset"
class_names = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

with open("herb_classes.json", "w") as f:
    json.dump(class_names, f, indent=4)

print("Class names saved to herb_classes.json")
