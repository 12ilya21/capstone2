from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Bookmark, RestaurantInfo1
from .serializers import BookmarkSerializer
from django.db import IntegrityError
from member.models import User

# 북마크 생성
class UserBookmarkCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        restaurant_name = request.data.get('restaurant_name')
        
        if not restaurant_name:
            return Response({"error": "restaurant_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Try to get or create a new bookmark
            bookmark, created = Bookmark.objects.get_or_create(user=user, name=restaurant)
            
            if created:
                # Increment the bookmark count for the restaurant
                restaurant.bookmark_count += 1
                restaurant.save()

            # Serialize the bookmark (newly created or existing)
            serializer = BookmarkSerializer(bookmark)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # This should never be reached due to the use of get_or_create
            return Response({"error": "Bookmark already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
# 북마크 삭제
class UserBookmarkDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        restaurant_name = request.data.get('restaurant_name')

        if not restaurant_name:
            return Response({"error": "restaurant_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Find the bookmark to delete
            bookmark = Bookmark.objects.get(user=user, name=restaurant)
            bookmark.delete()

            # Decrement the bookmark count for the restaurant
            if restaurant.bookmark_count > 0:
                restaurant.bookmark_count -= 1
                restaurant.save()

            return Response({"message": "Bookmark deleted successfully"}, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "An error occurred while deleting the bookmark"}, status=status.HTTP_400_BAD_REQUEST)
        
# 북마크 표시
class BookmarkListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookmarks = Bookmark.objects.filter(user=user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)