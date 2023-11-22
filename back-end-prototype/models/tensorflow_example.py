import tensorflow as tf
import pandas as pd
import numpy as np

def load_and_preprocess_data(data):
    # Load the data
    return data  # assuming coords is the preprocessed data

# insert your trained tensor flow model here and  make sure pathing is correct
def apply_model(data_for_model, model_path='my_model.h5'):
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Get the new coordinates from the model
    new_results = model.predict(data_for_model)
    
    return new_results

def save_data(organized_data, output_file_path):
    with pd.ExcelWriter(output_file_path) as writer:
        organized_data.to_excel(writer)
    print("successfully saved")


def call_model(data):
    # Step 1: Preprocess the messy data
    data_for_model = load_and_preprocess_data(data)

    # Step 2: we load model and predict & rearrage the data
    new_results = apply_model(data_for_model)

    # Step 3: Save the organized data to data base
    output_file_path = r'E:\NittanyAI Projects\Nittany-AI-Rapid-Prototyping-Code\back-end-prototype\results'
    save_data(new_results, output_file_path)