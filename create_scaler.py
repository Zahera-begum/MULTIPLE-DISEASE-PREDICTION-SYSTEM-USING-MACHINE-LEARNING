import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
import os

folder = os.path.dirname(os.path.abspath(__file__))
scaler = StandardScaler()
# Standard ranges for Heart Disease features
dummy_data = np.array([[50, 1, 1, 120, 200, 0, 1, 150], [20, 0, 0, 90, 150, 0, 0, 100]])
scaler.fit(dummy_data)

joblib.dump(scaler, os.path.join(folder, 'heart_scaler.pkl'))
print("SUCCESS: heart_scaler.pkl created in disease_api folder!")