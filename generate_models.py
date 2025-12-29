import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def create_placeholder_model(name, features_count):
    # Create dummy data to train a basic model
    X = np.random.rand(100, features_count)
    y = np.random.randint(0, 2, 100)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier()
    model.fit(X_scaled, y)
    
    # Save according to the names expected by views.py
    joblib.dump(model, f'{name}_model.pkl')
    joblib.dump(scaler, f'{name}_scaler.pkl')
    print(f"Generated: {name}_model.pkl and {name}_scaler.pkl")

# Based on standard datasets:
create_placeholder_model('heart', 13)    # Heart typically uses 13 features
create_placeholder_model('liver', 10)    # Liver typically uses 10 features
create_placeholder_model('diabetes', 8)  # Diabetes typically uses 8 features