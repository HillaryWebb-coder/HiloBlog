from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list_view, name='post_list'),
    path('tag/<slug:tag_slug>',	views.post_list_by_tag_view,
         name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.single_post_view, name='post_detail'),
    path('share/<int:post_id>', views.post_share_view, name="share_view"),
    path('feed/', LatestPostFeed(), name="post_feed"),
]
