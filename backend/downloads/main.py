import matplotlib
matplotlib.use('Agg')
from satellite_img_fetcher import fetch_satellite_image
from matplt_graph import process_ndvi
from data import data_file
from flask import Flask,jsonify, send_from_directory
from flask_cors import CORS
import os


years = list(range(2015, 2025))

# Fetch images for all years
for year in years:
    fetch_satellite_image(year)

# Process NDVI values and plot the trend for graph showing the NDVI trend for the Amazon rainforest deforestation
process_ndvi()
data_file()

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_FOLDER = os.path.join(BASE_DIR, "downloads")  # Ensure full path
OUTPUT_FOLDER = os.path.join(BASE_DIR, "downloads") 

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_heatmap(image_filename, output_filename):
    """Generates and saves a heatmap of a single image."""
    
    # Construct full file paths
    image_path = os.path.join(DATA_FOLDER, image_filename)
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Debugging: Print file paths
    print(f"📂 Processing Image: {image_path}")

    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        return None

    # Load image
    image = cv2.imread(image_path)

    # Ensure image loaded properly
    if image is None:
        print(f"❌ Error: Could not read {image_path}. Check if it's a valid image!")
        return None

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply heatmap color map
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # Save the heatmap image
    cv2.imwrite(output_path, heatmap)
    print(f"✅ Heatmap saved at: {output_path}")

    # Display the heatmap
    plt.imshow(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))
    plt.title(f"Heatmap for {image_filename}")
    plt.axis("off")
    plt.show()

    return output_path

# 🔥 Generate heatmaps for 2015 & 2024 images separately
generate_heatmap("amazon_2015.png", "heatmap_2015.png")
generate_heatmap("amazon_2024.png", "heatmap_2024.png")







app = Flask(__name__)
CORS(app, resources={r"/images/*": {"origins": "*"}})

DOWNLOADS_FOLDER = os.path.join(os.getcwd(), "downloads")

# Ensure the folder exists
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route('/images')
def list_images():
    """Returns a list of image URLs from the downloads folder."""
    images = [
        {"name": img, "url": f"http://127.0.0.1:5000/images/{img}"}
        for img in os.listdir(DOWNLOADS_FOLDER)
        if img.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    return jsonify({"images": images})

@app.route('/images/<path:filename>')  # Ensure path handling
def get_image(filename):
    """Serves an image file from the downloads folder."""
    return send_from_directory(DOWNLOADS_FOLDER, filename, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)