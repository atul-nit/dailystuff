from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('servicereviews/<int:service_id>/', views.serviceReviews, name='serviceReviews'),
    path('add_review_rating/<int:service_id>/', views.addReviewRating, name='addReviewRating'),
]