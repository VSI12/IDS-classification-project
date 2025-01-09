import base64
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from models import modelRFC, modelDTC, modelKNN, modelGNB
from datetime import datetime
from flask import request, jsonify

import warnings
warnings.filterwarnings('ignore')

np.set_printoptions(precision=3)
sns.set_theme(style="darkgrid")
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

col_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]

label_mapping = {
    0: "Normal",      # Normal traffic
    1: "DoS",         # Denial of Service attacks
    2: "R2L",         # Remote to Local attacks
    3: "U2R",         # User to Root attacks
    4: "Probe"        # Probe attacks (scanning for vulnerabilities)
}

def preprocess(dataset):
    try:
        from models import X_columns
        processed_data = pd.read_csv(dataset, header=None, names=col_names)
        print("Initial dataset shape:", processed_data.shape)

        processed_data = pd.get_dummies(processed_data)
        print("Dataset after get_dummies:", processed_data.shape)

        processed_data = processed_data.reindex(columns = X_columns, fill_value=0)
        print("Dataset after reindex:", processed_data.shape)
    except Exception as e:
        print(f"Error preprocessing data: {str(e)}")
        return None

    return processed_data, 200

def models(processed_data):
    try:
        model = request.json.get("model")
        if model == "model_1":
            DecisionTree(processed_data)
        elif model == "model_2":
            RandomForest(processed_data)
        elif model == "model_3":
            KNN(processed_data)
        elif model == "model_4":  # For GaussianNB
            GaussianNB(processed_data)
        else:
            return jsonify({"error": "Invalid model selected"}), 400
        
    except Exception as e:
        print(f"Error generating predictions: {str(e)}")
        return none
    
    return img_base64, 200
#DECISION TREE CLASSIFIER
def DecisionTree(new_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    predictions = modelDTC.predict(new_data)
    predicted_labels = [label_mapping.get(pred, "Unknown") for pred in predictions]

    # Create a DataFrame for better visualization
    results_df = pd.DataFrame({'Predicted Label': predicted_labels})
    label_counts = results_df['Predicted Label'].value_counts()

    # Plotting the distribution of predictions
    fig, ax = plt.subplots()
    label_counts.plot(kind='bar', ax=ax, title='Distribution of Predictions')
    ax.set_xlabel('Attack Type')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    filename = f'Plot_DecisionTree({timestamp}).png'
    fig.savefig(filename)

    #Convert plot to base64 for display in HTML
    with open(filename, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    return img_base64

def RandomForest(new_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    predictions = modelRFC.predict(new_data)
    predicted_labels = [label_mapping.get(pred, "Unknown") for pred in predictions]

    # Create a DataFrame for better visualization
    results_df = pd.DataFrame({'Predicted Label': predicted_labels})
    label_counts = results_df['Predicted Label'].value_counts()

    # Plotting the distribution of predictions
    fig, ax = plt.subplots()
    label_counts.plot(kind='bar', ax=ax, title='Distribution of Predictions')
    ax.set_xlabel('Attack Type')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    filename = f'Plot_RandomForest({timestamp}).png'
    fig.savefig(filename)

    #Convert plot to base64 for display in HTML
    with open(filename, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    return img_base64

def KNN(new_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    predictions = modelKNN.predict(new_data)
    predicted_labels = [label_mapping.get(pred, "Unknown") for pred in predictions]

    # Create a DataFrame for better visualization
    results_df = pd.DataFrame({'Predicted Label': predicted_labels})
    label_counts = results_df['Predicted Label'].value_counts()

    # Plotting the distribution of predictions
    fig, ax = plt.subplots()
    label_counts.plot(kind='bar', ax=ax, title='Distribution of Predictions')
    ax.set_xlabel('Attack Type')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    filename = f'Plot_KNN({timestamp}).png'
    fig.savefig(filename)

    #Convert plot to base64 for display in HTML
    with open(filename, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    return img_base64

def GaussianNB(new_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    predictions = modelGNB.predict(new_data)
    predicted_labels = [label_mapping.get(pred, "Unknown") for pred in predictions]

    # Create a DataFrame for better visualization
    results_df = pd.DataFrame({'Predicted Label': predicted_labels})
    label_counts = results_df['Predicted Label'].value_counts()

    # Plotting the distribution of predictions
    fig, ax = plt.subplots()
    label_counts.plot(kind='bar', ax=ax, title='Distribution of Predictions')
    ax.set_xlabel('Attack Type')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    filename = f'Plot_GaussianNB({timestamp}).png'
    fig.savefig(filename)

    #Convert plot to base64 for display in HTML
    with open(filename, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    return img_base64