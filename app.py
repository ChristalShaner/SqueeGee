from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import logging
import numpy as np
from scipy.stats import zscore

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure logging file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/", methods=["GET", "POST"])
def home():
    original_data_preview = pd.DataFrame()
    cleaned_data = pd.DataFrame()
    change_info = {
        'removed_duplicates': 0,
        'missing_values': 0,
        'outliers_removed': 0,
        'rule_violations': 0,
        'messages': []
    }
    cleaned_file_path = None  

    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        missing_value_strategy = request.form.get("missing_values", "drop")
        duplicate_handling = request.form.get("duplicate_handling", "drop")
        outlier_removal = request.form.get("outlier_removal", "none")
        z_threshold = float(request.form.get("z_threshold", 3))
        no_negative_values = request.form.get("no_negative_values", "").split(',')
        max_values = {item.split('=')[0]: float(item.split('=')[1]) for item in request.form.get("max_values", "").split(',') if '=' in item}
        allowed_categories = {item.split('=')[0]: item.split('=')[1].split('|') for item in request.form.get("allowed_categories", "").split(',') if '=' in item}

        if file.filename:
            try:
                # Read CSV in chunks to optimize memory usage
                chunk_size = 10000 
                chunks = pd.read_csv(file, chunksize=chunk_size)
                original_data = pd.concat(chunks, ignore_index=True)
                
                original_data_preview = original_data.head(5)
                cleaned_data = original_data.copy()

                # Handle duplicates
                if duplicate_handling == "drop":
                    cleaned_data = cleaned_data.drop_duplicates().reset_index(drop=True)
                elif duplicate_handling == "keep_first":
                    cleaned_data = cleaned_data.drop_duplicates(keep='first').reset_index(drop=True)
                elif duplicate_handling == "keep_last":
                    cleaned_data = cleaned_data.drop_duplicates(keep='last').reset_index(drop=True)
                change_info['removed_duplicates'] = original_data.shape[0] - cleaned_data.shape[0]

                # Handle missing values
                if missing_value_strategy == "drop":
                    cleaned_data = cleaned_data.dropna()
                    change_info['messages'].append("Dropped rows with missing values.")
                elif missing_value_strategy == "ffill":
                    cleaned_data = cleaned_data.fillna(method='ffill')
                    change_info['messages'].append("Imputed missing values using forward fill.")
                
                # Remove outliers using Z-score
                if outlier_removal == "zscore":
                    numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
                    z_scores = np.abs((cleaned_data[numeric_columns] - cleaned_data[numeric_columns].mean()) / cleaned_data[numeric_columns].std())
                    cleaned_data = cleaned_data[(z_scores < z_threshold).all(axis=1)]
                    change_info['outliers_removed'] = original_data.shape[0] - cleaned_data.shape[0]

                # Apply custom rules (vectorized for efficiency)
                rule_violations = 0
                if no_negative_values:
                    no_negative_values = [col for col in no_negative_values if col in cleaned_data.columns]
                    rule_violations += (cleaned_data[no_negative_values] < 0).sum().sum()
                    cleaned_data[no_negative_values] = cleaned_data[no_negative_values].clip(lower=0)

                for col, max_val in max_values.items():
                    if col in cleaned_data.columns:
                        rule_violations += (cleaned_data[col] > max_val).sum()
                        cleaned_data[col] = cleaned_data[col].clip(upper=max_val)

                for col, categories in allowed_categories.items():
                    if col in cleaned_data.columns:
                        rule_violations += (~cleaned_data[col].isin(categories)).sum()
                        cleaned_data = cleaned_data[cleaned_data[col].isin(categories)]
                
                change_info['rule_violations'] = rule_violations

                # Save cleaned data
                cleaned_file_path = os.path.join(UPLOAD_FOLDER, "cleaned_data.csv")
                cleaned_data.to_csv(cleaned_file_path, index=False)

                # Update change info
                change_info['missing_values'] = original_data.isnull().sum().sum()

            except Exception as e:
                error_message = f"Error: {str(e)}"
                change_info['messages'].append(error_message)
                logging.error(error_message)

    return render_template('index.html', 
                           original_data=original_data_preview, 
                           cleaned_data=cleaned_data.head(5), 
                           change_info=change_info, 
                           cleaned_file_path=cleaned_file_path)

@app.route("/download")
def download_file():
    """Allow users to download the cleaned CSV file."""
    file_path = os.path.join(UPLOAD_FOLDER, "cleaned_data.csv")
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    # from waitress import serve  # Use a production-ready server
    # print("Running server on http://127.0.0.1:5000")
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True, threaded=True, use_reloader=False)
