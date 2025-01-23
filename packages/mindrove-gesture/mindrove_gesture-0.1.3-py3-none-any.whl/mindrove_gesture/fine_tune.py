from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from keras.models import Model
import pickle
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fine_tune_svm(
    model, 
    recorded_data, 
    recorded_labels, 
    svm_path,
    scaler_path,
    C=10.0, 
    kernel='linear', 
    gamma='scale', 
):
    """
    Fine-tunes the SVM model using the recorded data.
    
    Args:
        model (keras.models.Model): Feature extractor model.
        recorded_data (list): List of recorded data.
        recorded_labels (list): List of recorded labels.
        svm_path (str): Path to save the SVM model.
        scaler_path (str): Path to save the scaler.
        C (float): Regularization parameter.
        kernel (str): SVM kernel.
        gamma (str): Kernel coefficient.
        
        Returns:
            tuple: (SVM model, Scaler, Validation accuracy)        
    """
    # Split data into training and validation
    X_train, X_val, y_train, y_val = train_test_split( np.array(recorded_data), np.array(recorded_labels), test_size=0.2, random_state=42)

    # Feature extraction
    feature_extractor = Model(inputs=model.input, outputs=model.get_layer("dense_8").output)
    features_train = feature_extractor.predict(X_train)
    features_val = feature_extractor.predict(X_val)

    # Scaling features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(features_train)
    X_val_scaled = scaler.transform(features_val)
    logging.info("Data preprocessed and scaled.")

    # SVM model training
    svm = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)
    svm.fit(X_train_scaled, y_train)
    logging.info("SVM model trained.")

    # Save the SVM model and scaler
    with open(svm_path, "wb") as f:
        pickle.dump(svm, f)
        logging.info("SVM model saved.")

    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
        logging.info("Scaler saved.")

    # Validation accuracy
    val_accuracy = svm.score(X_val_scaled, y_val)
    logging.info(f"Validation accuracy: {val_accuracy}")
    if val_accuracy < 0.60:
        logging.info("Validation accuracy is lower than 60%. Please check your device and record the data again.")

    return svm, scaler, val_accuracy
