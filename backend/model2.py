# train_kmeans_pixels.py
import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import joblib

def collect_pixels_from_folder(folder, size=(128, 128)):
    all_pixels = []
    for file in os.listdir(folder):
        try:
            path = os.path.join(folder, file)
            img = Image.open(path).convert("RGB").resize(size)
            data = np.array(img).reshape(-1, 3)
            all_pixels.append(data)
        except:
            pass
    return np.vstack(all_pixels)

# Load pixel data
pixels_deforestation = collect_pixels_from_folder("data/deforestation")
pixels_forest = collect_pixels_from_folder("data/no_deforestation")

all_pixels = np.vstack([pixels_deforestation, pixels_forest])

# Train KMeans on pixel RGBs
kmeans_pixel = KMeans(n_clusters=2, random_state=42)
kmeans_pixel.fit(all_pixels)

# Save the pixel model
joblib.dump(kmeans_pixel, "kmeans_pixel_model.pkl")
print("Pixel-based KMeans model saved.")
