# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
import markdown
from .models import Post, Category
from comments.forms import CommentForm

# for class view import
from django.views.generic import ListView

# def index(request):
    # post_list = Post.objects.all()
    # return render(request, 'myblog/index.html', context = {
        # 'post_list': post_list,
        # })

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.increase_views()

    post.body = markdown.markdown(post.body,
            extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                ])

    form = CommentForm
    comment_list = post.comment_set.all()
    context = {'post': post,
            'form': form,
            'comment_list': comment_list
            }
    return render(request, 'myblog/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year = year,
            created_time__month = month)
    return render(request, 'myblog/index.html', context = {'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'myblog/index.html', context = {'post_list': post_list})

class IndexView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'

