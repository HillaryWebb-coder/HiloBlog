from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    title = "Blog"
    link = reverse_lazy("blog:post_list")
    description = "Latest Posts"

    def items(self):
        return Post.published.all()

    def items_title(self, item):
        return item.title

    def items_description(self, item):
        return truncatewords(item.content, 30)
