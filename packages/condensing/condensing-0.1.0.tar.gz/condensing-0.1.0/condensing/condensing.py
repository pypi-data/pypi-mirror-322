import numpy as np
from queue import Queue

from sklearn.cluster import KMeans
import pandas as pd

def is_homogeneous(data):
    """
    Check if all points in the data belong to the same class.
    The last column of each row is assumed to be the class label.

    Args:
        data (list or array-like): 2D structure where each row
                                   represents a sample and the last
                                   column is the class label.

    Returns:
        bool: True if all rows have the same class label, False otherwise.
    """
    # Convert to NumPy array to handle indexing consistently
    data = np.array(data)
    # Check if data is empty
    if data.size == 0:
        return False
    # Extract class labels (last column)
    classes = data[:, -1]
    # If there's only one unique class, it's homogeneous
    return len(np.unique(classes)) == 1

def compute_mean(data):
    """
    Compute the mean of a dataset, ignoring the class labels.
    Args:
    - data: List of points with features and class labels.

    Returns:
    - The mean of the features, with the class label appended.
    """
    # Convert to NumPy array to handle indexing consistently
    data = np.array(data)
    # Extract features (all columns except the last one)
    features = data[:, :-1]
    # Compute mean of features
    mean_features = np.mean(features, axis=0)
    # Extract class labels (last column)
    class_labels = data[:, -1]
    # Append the most frequent class label to the mean features
    most_frequent_class = np.bincount(class_labels.astype(int)).argmax()
    return np.append(mean_features, most_frequent_class)

def compute_class_means(data):
    """
    Compute the mean for each class in the dataset.
    Args:
    - data: List of points with features and class labels.

    Returns:
    - A list of class means, where each mean includes its class label.
    """
    unique_classes = {point[-1] for point in data}
    class_means = []
    for cls in unique_classes:
        class_data = [point[:-1] for point in data if point[-1] == cls]
        class_mean = np.mean(class_data, axis=0)
        class_means.append(np.append(class_mean, cls))
    return class_means

def construct_condensing_set(training_set):
    """
    Construct the condensing set (CS) from the training set (TS) using K-Means.
    Args:
    - training_set: List of data points with features and class labels.

    Returns:
    - condensing_set: A list of representative points forming the condensing set.
    """
    # Stage 1: Queue Initialization
    queue = Queue()

    # Ensure training_set is a 2D array:
    if isinstance(training_set, pd.DataFrame):
        training_set = training_set.to_numpy()
    if training_set.ndim == 1:  # Check if it's a 1D array
        training_set = training_set.reshape(1, -1)  # Reshape to 2D

    queue.put(training_set)
    condensing_set = []

    # Stage 2: Construction of the Condensing Set
    while not queue.empty():
        current_set = queue.get()  # Dequeue a subset of data

        # Step 8: Check if the set is homogeneous
        if is_homogeneous(current_set):
            mean_point = compute_mean(current_set)  # Compute the mean of C
            condensing_set.append(mean_point)  # Add to the condensing set
        else:
            # Step 12: Compute class means
            class_means = compute_class_means(current_set)
            initial_means = np.array([mean[:-1] for mean in class_means])  # Exclude class labels for K-Means

            # Step 17: Perform K-Means clustering
            features = np.array([point[:-1] for point in current_set])
            n_clusters = len(class_means)
            kmeans = KMeans(n_clusters=n_clusters, init=initial_means, n_init=1, random_state=42)
            labels = kmeans.fit_predict(features)

            # Step 18-20: Group points into new clusters and enqueue them
            new_clusters = [[] for _ in range(n_clusters)]
            for idx, point in enumerate(current_set):
                new_clusters[labels[idx]].append(point)

            for cluster in new_clusters:
                if cluster:  # Only enqueue non-empty clusters
                    queue.put(cluster)

    return condensing_set