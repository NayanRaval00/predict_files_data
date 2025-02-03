import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from flask import Flask, request, jsonify
import pickle

# Load Data (Replace with your database connection logic)
data = pd.read_csv("projects.csv")  # Assuming CSV for simplicity

# Data Preprocessing
data = data.dropna()  # Remove missing values
X = data[['project_team_size', 'project_estimate_time']]  # Features
y = data['project_actual_completion_time']  # Target variable

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save Model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Evaluate Model
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))

# Flask API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    team_size = data['project_team_size']
    estimate_time = data['project_estimate_time']
    
    # Load Model
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    
    prediction = model.predict(np.array([[team_size, estimate_time]]))
    return jsonify({"predicted_completion_time": prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
