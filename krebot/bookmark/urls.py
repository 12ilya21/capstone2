from django.urls import path
from .views import UserBookmarkCreateView, UserBookmarkDeleteView, BookmarkListView

urlpatterns = [
    path('create/', UserBookmarkCreateView.as_view(), name='create-bookmark'),
    path('delete/', UserBookmarkDeleteView.as_view(), name='delete-bookmark'),
    path('list/', BookmarkListView.as_view(), name='show-bookmark')
]