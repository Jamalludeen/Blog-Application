from django.urls import path
from .feed import LatestPostFeed
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('recent-posts/', views.recent_post, name='recent_post'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search-post/', views.search_post, name="search_post"),
    
]
