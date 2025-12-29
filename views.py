import os
import joblib
import numpy as np
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Feedback, Hospital

# --- AUTHENTICATION ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# --- DISEASE PREDICTION ---
class UnifiedPredictorView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        disease_type = request.data.get('type') 
        medical_data = request.data.get('medical_data')
        
        # Path to models folder
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_PATH, f'{disease_type}_model.pkl')
        scaler_path = os.path.join(BASE_PATH, f'{disease_type}_scaler.pkl')

        try:
            # Load and predict
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            input_arr = np.array([float(x) for x in medical_data]).reshape(1, -1)
            scaled_data = scaler.transform(input_arr)
            prediction = model.predict(scaled_data)
            
            result = "High Risk" if prediction[0] == 1 else "Low Risk"
            
            # Fetch real hospitals from Database if High Risk
            hospitals = []
            if result == "High Risk":
                hospital_objs = Hospital.objects.all()[:3] # Get first 3 hospitals
                hospitals = [{"name": h.name, "contact": h.contact} for h in hospital_objs]
                
                # Fallback if DB is empty
                if not hospitals:
                    hospitals = [{"name": "Creativity General Hospital", "contact": "+91 94831 75986"}]
            
            return Response({
                "risk_status": result,
                "recommendation": "Urgent specialist consultation advised." if result == "High Risk" else "Healthy results!",
                "hospitals": hospitals
            })
        except Exception as e:
            return Response({"error": "Model files missing. Please run fix_models.py"}, status=status.HTTP_400_BAD_REQUEST)

# --- CHATBOT (FIXED KEYWORD LOGIC) ---
class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        query = request.data.get('query', '').lower()
        if not query:
            return Response({"reply": ""})

        knowledge = {
            "heart": "Maintain LDL cholesterol below 100mg/dL and exercise 150 mins/week.",
            "diabetes": "Keep your HbA1c below 7.0% and monitor glucose daily.",
            "liver": "Avoid excessive alcohol and maintain a healthy weight."
        }
        
        # Default response
        reply = "I'm not sure about that. Please ask specifically about heart, liver, or diabetes health."
        
        # Loop through keys to find a match in the user's sentence
        for key in knowledge:
            if key in query:
                reply = knowledge[key]
                break 

        return Response({"reply": reply})

# --- FEEDBACK ---
class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        message = request.data.get('message')
        if message:
            Feedback.objects.create(user=request.user, message=message)
            return Response({"message": "Feedback submitted successfully!"})
        return Response({"error": "Empty message"}, status=status.HTTP_400_BAD_REQUEST)