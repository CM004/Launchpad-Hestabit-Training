import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32") #converts data into pixel values (for images) and input IDs (for text) as the model expects this
device = "cuda" if torch.cuda.is_available() else "cpu" #sets device to GPU if available, else CPU
model.to(device)

def embed_image(image_path):
    image = Image.open(image_path).convert("RGB") #load images from path and convert them into rgb format
    inputs = processor(images=image, return_tensors="pt").to(device) #creates embedding vectors and return pytorch tensors
    with torch.no_grad(): #disables gradient calculation
        features = model.get_image_features(**inputs) #get_image_features is a method in CLIPModel that extracts image features
    return features.cpu().numpy()[0]

def embed_text(text):
    inputs = processor(text=text, return_tensors="pt").to(device)
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    return features.cpu().numpy()[0]
