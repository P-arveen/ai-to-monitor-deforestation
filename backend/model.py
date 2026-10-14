import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
from PIL import Image
import joblib 

def preprocess_image(image_path, size=(128, 128)):
    """Resize, normalize and flatten the image to use it in the model"""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size)  # Resize image to reduce complexity
    img = np.array(img)  # Convert image to numpy array
    img = img / 255.0  # Normalize pixel values to [0, 1]
    return img.flatten()  # Flatten image to 1D array

def load_images_from_folder(folder, label, size=(128, 128)):
    """Load all images from a folder and assign them a label"""
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        try:
            img_data = preprocess_image(img_path, size)
            images.append(img_data)
            labels.append(label)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    return images, labels

# Load the training and testing datasets
folder_1 = "processed_data/deforestation"  # e.g., deforested images
folder_2 = "processed_data/no_deforestation"  # e.g., non-deforested images

# Load images and labels
X_class_1, y_class_1 = load_images_from_folder(folder_1, label=0)
X_class_2, y_class_2 = load_images_from_folder(folder_2, label=1)

# Combine both classes
X = np.array(X_class_1 + X_class_2)
y = np.array(y_class_1 + y_class_2)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply feature scaling (normalize the data)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # Fit and transform on train data
X_test = scaler.transform(X_test)  # Only transform on test data

# Initialize and train the Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))  # Detailed evaluation report
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model and predictions
joblib.dump(rf_model, "rf_model.pkl")
np.save('y_test.npy', y_test)
np.save('y_pred.npy', y_pred)

# Example of predicting a new image
def predict_image(model, image_path, size=(128, 128)):
    """Predict the class of a new image"""
    img_data = preprocess_image(image_path, size)
    img_data = scaler.transform([img_data])  # Scale the image before predicting
    prediction = model.predict(img_data)
    return prediction

# Example of predicting a new image
new_image_path = "test4.jpg"  # Path to the new image
prediction = predict_image(rf_model, new_image_path)
print("Predicted class:", "Deforested" if prediction[0] == 0 else "Non-Deforested")
