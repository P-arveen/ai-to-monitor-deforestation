import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import joblib
# Step 1: Preprocessing Image
def preprocess_image(image_path, size=(128, 128)):
    """Resize and flatten the image to prepare for KMeans"""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size) 
    img = np.array(img) 
    return img.flatten()  

# Step 2: Load Images from a Folder (only process image files)
def load_images_from_folder(folder, size=(128, 128)):
    """Load all images from a folder and preprocess them"""
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path) and img_path.lower().endswith(('.png', '.jpg', '.jpeg')):  
            try:
                img_data = preprocess_image(img_path, size)
                images.append(img_data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return np.array(images)

# Step 3: Perform KMeans Clustering
def perform_kmeans_clustering(X, n_clusters=2):
    """Cluster the data into 'n_clusters' groups using KMeans"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    return kmeans

# Step 4: Prediction on New Image
def predict_image(image_path, kmeans_model):
    """Predict whether the new image is deforested or non-deforested"""
    img_data = preprocess_image(image_path)
    prediction = kmeans_model.predict([img_data])  
    
    # Return predicted class based on the cluster
    if prediction[0] == 0:
        return "Deforested"
    else:
        return "Non-Deforested"


if __name__ == "__main__":
 
    folder_1 = "data/deforestation" 
    folder_2 = "data/no_deforestation"  

  
    print("Loading deforested images...")
    X_class_1 = load_images_from_folder(folder_1)
    print(f"Loaded {X_class_1.shape[0]} deforested images.")

    print("Loading non-deforested images...")
    X_class_2 = load_images_from_folder(folder_2)
    print(f"Loaded {X_class_2.shape[0]} non-deforested images.")

    # Combine both sets of images into one dataset
    X = np.concatenate((X_class_1, X_class_2), axis=0)

    # Perform KMeans clustering
    print("Performing KMeans clustering...")
    kmeans = perform_kmeans_clustering(X, n_clusters=2)

    print("Clustering completed.")
    print(f"Cluster centers:\n{kmeans.cluster_centers_}")

   
    labels = kmeans.labels_
    cluster_0 = np.where(labels == 0)[0]
    cluster_1 = np.where(labels == 1)[0]

    # Print results
    print(f"Cluster 0 (Assumed Deforested): {len(cluster_0)} images")
    print(f"Cluster 1 (Assumed Non-Deforested): {len(cluster_1)} images")

    # Optional: Save the results (cluster labels, centers, etc.) for later analysis
    np.save('cluster_labels.npy', labels)
    np.save('cluster_centers.npy', kmeans.cluster_centers_)
    print("Cluster results saved.")
    
    joblib.dump(kmeans, 'kmeans_model.pkl')
    # Predict a new image
    new_image_path = 'test4.png'  # Path to your new image
    predicted_class = predict_image(new_image_path, kmeans)

    # Display the new image and prediction
    img = Image.open(new_image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"Predicted Class: {predicted_class}")
    plt.show()

    # If you have true labels (for demo purposes, use a placeholder true_label)
    true_label = "Deforested"  # Replace with actual true label if available

    # Map the predicted label to a numerical format (0 for deforested, 1 for non-deforested)
    predicted_label = 0 if predicted_class == "Deforested" else 1
    true_label_num = 0 if true_label == "Deforested" else 1

    # Calculate accuracy for the new prediction (if true label is known)
    accuracy = accuracy_score([true_label_num], [predicted_label])
    print(f"Accuracy of the new prediction: {accuracy * 100:.2f}%")
