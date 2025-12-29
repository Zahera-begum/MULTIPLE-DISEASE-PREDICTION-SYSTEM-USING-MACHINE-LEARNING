import joblib
import numpy as np
import os

def predict_disease(data, disease_type):
    try:
        # Get the path to the heart_model.pkl file you just created
        model_path = os.path.join(os.path.dirname(__file__), 'heart_model.pkl')
        
        # Load the binary model [cite: 59]
        model = joblib.load(model_path)
        
        # Convert the medical data into a format the model understands [cite: 61, 62]
        input_data = np.array([float(x) for x in data]).reshape(1, -1)
        
        # Make a real prediction using the model [cite: 49, 102]
        prediction = model.predict(input_data)
        
        # 1 means High Risk, 0 means Low Risk [cite: 17, 50]
        return "High Risk" if prediction[0] == 1 else "Low Risk"
    except Exception as e:
        return f"Error: {str(e)}"