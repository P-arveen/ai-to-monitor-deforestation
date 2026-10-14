import matplotlib
matplotlib.use('Agg')
from satellite_img_fetcher import fetch_satellite_image
from matplt_graph import process_ndvi
from data import data_file
from aveg_tem_change import  get_year_avg
from flask import Flask,jsonify, send_from_directory, request
from flask_cors import CORS
import os
import joblib
import numpy as np
from PIL import Image
from sklearn.metrics import accuracy_score



# years = list(range(2015, 2025))

# # Fetch images for all years
# for year in years:
#     fetch_satellite_image(year)

# # Process NDVI values and plot the trend for graph showing the NDVI trend for the Amazon rainforest deforestation
# process_ndvi()
# data_file()

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# DATA_FOLDER = os.path.join(BASE_DIR, "downloads")  # Ensure full path
# OUTPUT_FOLDER = os.path.join(BASE_DIR, "downloads") 

# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# def generate_heatmap(image_filename, output_filename):
#     """Generates and saves a heatmap of a single image."""
    
#     # Construct full file paths
#     image_path = os.path.join(DATA_FOLDER, image_filename)
#     output_path = os.path.join(OUTPUT_FOLDER, output_filename)

#     # Debugging: Print file paths
#     print(f"📂 Processing Image: {image_path}")

#     # Check if image exists
#     if not os.path.exists(image_path):
#         print(f"❌ Error: File not found: {image_path}")
#         return None

#     # Load image
#     image = cv2.imread(image_path)

#     # Ensure image loaded properly
#     if image is None:
#         print(f"❌ Error: Could not read {image_path}. Check if it's a valid image!")
#         return None

#     # Convert image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply heatmap color map
#     heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

#     # Save the heatmap image
#     cv2.imwrite(output_path, heatmap)
#     print(f"✅ Heatmap saved at: {output_path}")

#     # Display the heatmap
#     plt.imshow(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))
#     plt.title(f"Heatmap for {image_filename}")
#     plt.axis("off")
#     plt.show()

#     return output_path

# # 🔥 Generate heatmaps for 2015 & 2024 images separately
# generate_heatmap("amazon_2015.png", "heatmap_2015.png")
# generate_heatmap("amazon_2024.png", "heatmap_2024.png")







app = Flask(__name__)
CORS(app)



DOWNLOADS_FOLDER = os.path.join(os.getcwd(), "downloads")
# Ensure the folder exists
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)


# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


kmeans_model = joblib.load('kmeans_model.pkl')
kmeans_pixel_model = joblib.load('kmeans_pixel_model.pkl')

def preprocess_image(file, size=(128, 128)):
    img = Image.open(file).convert("RGB")
    img = img.resize(size)
    return np.array(img).flatten()



def preprocess_image_pixels(image_path, size=(128, 128)):
    """Load and resize image, then reshape pixels into 2D array"""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size)
    data = np.array(img)
    pixels = data.reshape(-1, 3) 
    return pixels

def predict_forest_percent(image_path):
    pixels = preprocess_image_pixels(image_path)
    predictions = kmeans_pixel_model.predict(pixels)

  
    unique, counts = np.unique(predictions, return_counts=True)
    total = counts.sum()

    cluster_percentages = dict(zip(unique, (counts / total) * 100))

    #  cluster is forested/deforested
    forest_cluster = np.argmin(kmeans_pixel_model.cluster_centers_.mean(axis=1))
    deforest_cluster = 1 - forest_cluster

    forest_percent = cluster_percentages.get(forest_cluster, 0)
    deforest_percent = cluster_percentages.get(deforest_cluster, 0)

    return round(forest_percent, 2), round(deforest_percent, 2)

forest, deforest = predict_forest_percent("test2.jpg")
print(f"Forested Area: {forest}%")
print(f"Deforested Area: {deforest}%")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    try:
        forest_percent, deforest_percent = predict_forest_percent(file)
        img_data = preprocess_image(file)
        prediction = kmeans_model.predict([img_data])
        label = "Deforested" if prediction[0] == 0 else "Non-Deforested"
        return jsonify({"prediction": label,
                         "forest_percent": forest_percent,
                         "deforest_percent": deforest_percent})
    except Exception as e:
        import traceback
        traceback.print_exc()  
        return jsonify({"error": str(e)}), 500



@app.route("/temperature-india")
def temperature_india():
    try:
        avg_2023 = round(get_year_avg(2023), 2)
        avg_2024 = round(get_year_avg(2024), 2)
        change = round(avg_2024 - avg_2023, 2)

        return jsonify({
            "avg_2023": avg_2023,
            "avg_2024": avg_2024,
            "change": change
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



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



NDVI_FOLDER = os.path.join(os.getcwd(), "ndvi_outputs")
os.makedirs(NDVI_FOLDER, exist_ok=True)

@app.route('/ndvi_trend')
def get_ndvi_trend():
    """Serves the NDVI trend PNG."""
    return send_from_directory(NDVI_FOLDER, "ndvi_trend.png")




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEATMAP_FOLDER = os.path.join(BASE_DIR, "heatmaps")


if not os.path.exists(HEATMAP_FOLDER):
    os.makedirs(HEATMAP_FOLDER)

@app.route("/heatmaps", methods=["GET"])
def list_heatmaps():
    """Returns a list of available heatmap images"""
    heatmap_images = [
        {"name": img, "url": f"http://127.0.0.1:5000/heatmaps/{img}"}
        for img in os.listdir(HEATMAP_FOLDER)
        if img.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    return jsonify({"heatmaps": heatmap_images})

@app.route("/heatmaps/<filename>", methods=["GET"])
def get_heatmap(filename):
    """Serves a specific heatmap image"""
    return send_from_directory(HEATMAP_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)