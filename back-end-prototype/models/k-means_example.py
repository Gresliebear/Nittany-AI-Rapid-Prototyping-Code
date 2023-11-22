from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

def load_and_preprocess_data(data):
    # Load the data
    return data  # assuming coords is the preprocessed data

def apply_model(data, num_clusters):
    """
    Applies k-means clustering to the given data using the specified number of clusters.

    Parameters:
    data (array-like): The data to be clustered.
    num_clusters (int): The number of clusters to form.

    Returns:
    array: The cluster labels for each data point.
    """
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(data)
    return kmeans.labels_


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