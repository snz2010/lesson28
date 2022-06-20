from django.urls import path
from .views import AdUploadImageView, AdDeleteView, AdUpdateView, AdCreateView, AdView, AdDetailView

urlpatterns = [
    path('', AdView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImageView.as_view()),
]