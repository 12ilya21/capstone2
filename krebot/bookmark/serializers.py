from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    restaurant_name = serializers.CharField(source='name.name', read_only=True)

    class Meta:
        model = Bookmark
        fields = ['user', 'restaurant_name']