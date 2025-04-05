import shutil
import uuid
from pathlib import Path

# Root of your datasets
root_path = Path("dataset")
output_path = root_path / "merged"

# Ensure output root exists
output_path.mkdir(parents=True, exist_ok=True)

# Traverse all dataset folders
for dataset_folder in root_path.glob("dataset*"):
    if not dataset_folder.is_dir():
        continue

    # For each label folder
    for label_folder in dataset_folder.iterdir():
        if not label_folder.is_dir():
            continue

        label_name = label_folder.name
        target_label_path = output_path / label_name
        target_label_path.mkdir(parents=True, exist_ok=True)

        # For each file in the label folder
        for file in label_folder.glob("*.jpg"):
            # Generate a new unique name with same extension
            new_file_name = f"{uuid.uuid4()}{file.suffix}"
            target_file_path = target_label_path / new_file_name

            # Copy the file
            shutil.copy2(file, target_file_path)

print("Merging complete.")
