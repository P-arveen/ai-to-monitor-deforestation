import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# List of years from 2015 to 2024
years = list(range(2015, 2025))
image_dir = "downloads/"
output_dir = "ndvi_outputs/"  # Folder to save NDVI graphs
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Generate full paths for images
image_files = [os.path.join(image_dir, f"amazon_{year}.png") for year in years]

def calculate_ndvi(image_path):
    """Computes NDVI for a given image."""
    if not os.path.exists(image_path):
        print(f"Error: File not found -> {image_path}")
        return None  # Skip processing if the file is missing

    img = cv2.imread(image_path)  # Read image
    if img is None:
        print(f"Error: Unable to read the image -> {image_path}")
        return None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Extract Red and NIR channels
    red = img[:, :, 0].astype(float)  # Red band
    nir = img[:, :, 2].astype(float)  # NIR band

    # Compute NDVI
    ndvi = (nir - red) / (nir + red + 1e-6)

    return np.nanmean(ndvi)  # Return average NDVI

def process_ndvi():
    """Calculates NDVI for all images, saves the trend as PNG."""
    ndvi_values = [calculate_ndvi(image) for image in image_files]

    # Plot NDVI change over time
    plt.figure(figsize=(10, 5))
    plt.plot(years, ndvi_values, marker='o', linestyle='-', color='green', label="NDVI Trend")
    plt.axhline(y=0.5, color='r', linestyle='--', label="Healthy Forest Threshold")
    plt.xlabel("Year")
    plt.ylabel("Average NDVI")
    plt.title("Amazon Deforestation NDVI Trend (2015-2024)")
    plt.legend()
    plt.grid()

    # Save the plot as a PNG file
    output_path = os.path.join(output_dir, "ndvi_trend.png")
    plt.savefig(output_path, dpi=300)  # Save as high-resolution PNG
    print(f"NDVI trend graph saved at: {output_path}")
    plt.close()  # Close the plot to free memory

    return output_path  # Return file path

if __name__ == "__main__":
    process_ndvi()

