import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Create a dummy model for Heart Disease
X = np.random.rand(100, 4)  # 4 features
y = np.random.randint(0, 2, 100)
model = RandomForestClassifier()
model.fit(X, y)

# Save it to your api folder
joblib.dump(model, 'disease_api/heart_model.pkl')
print("Model saved as heart_model.pkl")