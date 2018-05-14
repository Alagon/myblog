# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from .models import Post

class AllPostRssFeed(Feed):
    title = "剑子仙迹的博客"
    link = "/"
    description = "剑子仙迹的学习记录文章"

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
