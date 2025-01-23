import threading
import numpy as np
import pickle
from keras.models import load_model, Model
from queue import Queue, Empty
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mindrove_gesture.utils import MyMagnWarping, MyScaling

def real_time_inference(
    feature_extractor_path,
    svm_model_path,
    scaler_path,
    filters,
    model_input_len=100,
    gyro_threshold=2000,
    prediction_threshold=0.4,
    batch_size=5,
):
    """
    Starts real-time inference and yields predictions.
    
    Args:
        feature_extractor_path (str): Path to the feature extractor model.
        svm_model_path (str): Path to the SVM model.
        scaler_path (str): Path to the scaler.
        filters (list): List of filters.
        model_input_len (int): Length of input data to the model.
        gyro_threshold (float): Threshold for gyro data to filter movement artifacts.
        prediction_threshold (float): Confidence threshold for predictions.
        batch_size (int): Number of samples to process in one batch.

    Yields:
        tuple: (prediction, confidence scores) in real time.
    """
    # Load the models and scaler
    feature_extractor = load_model(feature_extractor_path, custom_objects={"MyMagnWarping": MyMagnWarping, "MyScaling": MyScaling})
    feature_extractor = Model(inputs=feature_extractor.input, outputs=feature_extractor.get_layer("dense_8").output)
    with open(svm_model_path, "rb") as svm_file:
        svm = pickle.load(svm_file)
    with open(scaler_path, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)

    # Setup MindRove board
    BoardShim.enable_dev_board_logger()
    board_id = BoardIds.MINDROVE_WIFI_BOARD
    params = MindRoveInputParams()
    board_shim = BoardShim(board_id, params)
    
    # Setup data queue and thread controls
    data_queue = Queue()
    stop_event = threading.Event()
    output_queue = Queue()

    # Preprocessing function
    def preprocess_data(data):
        for i in range(len(data)):
            for ch in range(data.shape[1]):
                for filter_ in filters:
                    data[i, ch] = filter_.process(data[i, ch], ch)
        return data

    # Inference thread
    def inference_worker():
        inference_results = []
        while not stop_event.is_set():
            try:
                input_tensor = data_queue.get(timeout=1)
                features = feature_extractor.predict(input_tensor)
                features_scaled = scaler.transform(features)
                predictions = svm.predict_proba(features_scaled)
                inference_results.extend(predictions)

                if len(inference_results) >= batch_size:
                    avg_result = np.mean(inference_results, axis=0)
                    final_output = np.argmax(avg_result)
                    if avg_result[final_output] >= prediction_threshold:
                        output_queue.put((final_output, avg_result))
                    inference_results.clear()
            except Empty:
                continue

    # Start streaming from the MindRove board
    try:
        board_shim.prepare_session()
        board_shim.start_stream(450000)

        # Start inference thread
        inference_thread = threading.Thread(target=inference_worker, daemon=True)
        inference_thread.start()

        batch_of_data = []
        gyro_channels = BoardShim.get_gyro_channels(BoardIds.MINDROVE_WIFI_BOARD)

        while not stop_event.is_set():
            if board_shim.get_board_data_count() < model_input_len:
                continue

            raw_data = board_shim.get_board_data(model_input_len)
            emg_data = raw_data[:8]
            gyro_data = raw_data[gyro_channels]

            if np.any(gyro_data > gyro_threshold):
                batch_of_data = []
                continue

            processed_data = preprocess_data(emg_data.T)
            input_tensor = np.expand_dims(processed_data.T, axis=2).astype(np.float32)
            batch_of_data.append(input_tensor)

            if len(batch_of_data) == batch_size:
                data_queue.put(np.array(batch_of_data))
                batch_of_data = []

            # Yield predictions from the output queue
            while not output_queue.empty():
                yield output_queue.get()

    except Exception as e:
        raise RuntimeError(f"Error during real-time inference: {e}")

    finally:
        stop_event.set()
        board_shim.stop_stream()
        board_shim.release_session()
