from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from bookmark.models import RestaurantInfo1

# 식당 좌표 넘기기
class RestaurantCoordinatesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        restaurant_name = request.data.get('restaurant_name')
        
        if not restaurant_name:
            return Response({"error": "restaurant_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
            data = {
                "name": restaurant.name,
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
            }
            return Response(data, status=status.HTTP_200_OK)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)