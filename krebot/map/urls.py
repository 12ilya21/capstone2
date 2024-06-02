from django.urls import path
from .views import RestaurantCoordinatesView

urlpatterns = [
    path('coordinates/', RestaurantCoordinatesView.as_view()),
]