# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from myblog.models import Post
from .models import Comment
from .forms import CommentForm

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.name = request.user.username
            comment.email = request.user.email
            comment.post = post
            comment.save()

            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {'post': post,
                    'form': form,
                    'comment_list': comment_list
                    }
            return render(request, 'myblog/index.html', context = context)
    return redirect(post)

