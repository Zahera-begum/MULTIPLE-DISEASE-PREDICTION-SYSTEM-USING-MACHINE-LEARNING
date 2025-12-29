import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# This points to the subfolder where Django expects to find the models
TARGET_FOLDER = 'disease_api'

# Ensure the folder exists
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

def generate_and_save(name, feature_count):
    print(f"Generating models for: {name}...")
    
    # 1. Create dummy training data (X) and labels (y)
    # This simulates 100 patients with 'feature_count' health metrics
    X = np.random.rand(100, feature_count)
    y = np.random.randint(0, 2, 100) # 0 = Low Risk, 1 = High Risk
    
    # 2. Train the Model (Random Forest)
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    
    # 3. Train the Scaler (Normalizes the input data)
    scaler = StandardScaler()
    scaler.fit(X)
    
    # 4. Save files into the disease_api folder
    model_file = os.path.join(TARGET_FOLDER, f'{name}_model.pkl')
    scaler_file = os.path.join(TARGET_FOLDER, f'{name}_scaler.pkl')
    
    joblib.dump(model, model_file)
    joblib.dump(scaler, scaler_file)
    
    print(f"  -> Saved {model_file}")
    print(f"  -> Saved {scaler_file}")

# These counts MUST match the inputConfig fields in your React App.js
# Heart: 8 inputs, Liver: 6 inputs, Diabetes: 7 inputs
generate_and_save('heart', 8)
generate_and_save('liver', 6)
generate_and_save('diabetes', 7)

print("\nAll models generated successfully! You can now run your project.")