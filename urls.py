from django.urls import path
from .views import UnifiedPredictorView, ChatbotView, FeedbackView

urlpatterns = [
    path('predict/', UnifiedPredictorView.as_view(), name='predict'),
    path('chat/', ChatbotView.as_view(), name='chat'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]