import os
import sys
sys.path.append('src')

import json
import numpy as np
from pathlib import Path
from embeddings.clip_embedder import embed_image
from embeddings.blip_captioner import caption_image
import pytesseract 
from PIL import Image
from tqdm import tqdm

print("Starting Nested Image Ingest\n")

parent_dir = Path("src/data/images/EnterpriseRAG_2025_02_markdown")
images_data = []
count = 0

# Get list of folders first
folders = [f for f in parent_dir.iterdir() if f.is_dir()][:10]

# Loop through all folders with progress bar
for folder in tqdm(folders, desc="Processing folders"):
    
    # Find images in each folder
    for img_path in folder.rglob("*"):
        if img_path.suffix.lower() in ['.jpg', '.png', '.jpeg']:
            print(f"Processing {folder.name}/{img_path.name}...")
            try:
                ocr_text = pytesseract.image_to_string(Image.open(img_path)) #extracts text visible in images (tables, diagrams, labels)
                caption = caption_image(str(img_path)) #generates caption for image using blip 
                embedding = embed_image(str(img_path)) #generates image embedding using CLIP

                images_data.append({
                    "filename": img_path.name,
                    "folder": folder.name,
                    "ocr": ocr_text[:100],
                    "caption": caption,
                    "path": str(img_path)
                })

                Path("src/embeddings/image_embeddings").mkdir(exist_ok=True)
                np.save(f"src/embeddings/image_embeddings/image_{folder.name}_{img_path.stem}.npy", embedding)
                count += 1
                print(f"Caption: {caption}\n")
            except Exception as e:
                print(f"Error: {e}\n")

# Save metadata
Path("src/data/images_metadata").mkdir(exist_ok=True)
json.dump(images_data, open("src/data/images_metadata/images.json", "w"), indent=2)
print(f"Processed {len(images_data)} images from {len(list(parent_dir.iterdir()))} folders")
