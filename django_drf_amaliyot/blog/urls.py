from django.urls import path
from .views import create_post, update_post, get_post, delete_post, PostListApiView


urlpatterns = [
    path('list_posts/', PostListApiView.as_view(), ),
    path('create_post/', create_post, ),
    path('update_post/<int:pk>/', update_post, ),
    path('get_post/<int:pk>/', get_post, ),
    path('delete_post/<int:pk>/', delete_post, ),


]
