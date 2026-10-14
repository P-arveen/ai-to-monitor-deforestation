from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
from sentinelhub import (
    SHConfig, SentinelHubRequest, DataCollection, MimeType, BBox,
    bbox_to_dimensions, CRS, MosaickingOrder
)




config = SHConfig()
config.sh_client_id = "ab5ec6ea-7329-469b-8509-15eeadf6f653"
config.sh_client_secret = "eX5DYP09r5TTfBXUkxruUuXq1mfjnmny"

data_collection = DataCollection.LANDSAT_OT_L2  # ✅ Correct identifier
amazon_bbox = BBox(bbox=(-61.0, -3.0, -60.5, -2.5), crs=CRS.WGS84)
years = list(range(2015, 2024))

download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)


evalscript_true_color = """
function setup() {
    return {
        input: ["B04", "B03", "B02"],
        output: { bands: 3, sampleType: "FLOAT32" }
    };
}

function evaluatePixel(sample) {
    return [sample.B04 * 2.3, sample.B03 * 2.5, sample.B02 * 1.8];
}
"""
def fetch_satellite_image(year):
    """Fetches satellite image for a given year, using Sentinel-2 (2015+) or Landsat (2010-2014)."""
    filename = os.path.join(download_folder, f"amazon_{year}.png")

    # **Check if the image already exists**
    if os.path.exists(filename):
        print(f"✅ Image for {year} already exists. Skipping download.")
        return filename

    print(f"📡 Fetching image for {year}...")

    size = bbox_to_dimensions(amazon_bbox, resolution=100)

    # **Select the correct satellite data source**
    if year >= 2017:
        data_collection = DataCollection.SENTINEL2_L2A
    elif year >= 2015:
        data_collection = DataCollection.SENTINEL2_L1C
    elif year >= 2013:
       data_collection = DataCollection.LANDSAT_OT_L2  
    else:
       data_collection = DataCollection.LANDSAT_TM_L1  

    try:
        request = SentinelHubRequest(
            evalscript=evalscript_true_color,
            input_data=[SentinelHubRequest.input_data(
                data_collection=data_collection,
                time_interval=(f"{year}-06-01", f"{year}-08-31"),
                mosaicking_order=MosaickingOrder.LEAST_CC,
                maxcc=0.3
            )],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=amazon_bbox,
            size=size,
            config=config
        )

        response = request.get_data()
        if not response:
            print(f"❌ No data available for {year}")
            return None

        # Convert image data
        image = np.array(response[0], dtype=np.float32)

        def normalize_image(image):
            image = (image - np.percentile(image, 2)) / (np.percentile(image, 98) - np.percentile(image, 2))
            image = np.clip(image, 0, 1)
            return (image * 255).astype(np.uint8)

        image_normalized = normalize_image(image)

        # Save the image
        plt.imsave(filename, image_normalized)
        print(f"✅ Image for {year} downloaded and saved at {filename}!")
        return filename

    except Exception as e:
        print(f"⚠️ Error fetching image for {year}: {str(e)}")
        return None