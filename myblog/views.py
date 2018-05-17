# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
import markdown
from .models import Post, Category, Tag
from comments.forms import CommentForm

# for class view import
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .forms import PostPublishForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AdminRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AdminRequiredMixin, cls).as_view(**initkwargs)
        return staff_member_required(view)

# def index(request):
    # post_list = Post.objects.all()
    # return render(request, 'myblog/index.html', context = {
        # 'post_list': post_list,
        # })

# def detail(request, pk):
    # post = get_object_or_404(Post, pk = pk)
    # post.increase_views()

    # post.body = markdown.markdown(post.body,
            # extensions = [
                # 'markdown.extensions.extra',
                # 'markdown.extensions.codehilite',
                # 'markdown.extensions.toc',
                # ])

    # form = CommentForm
    # comment_list = post.comment_set.all()
    # context = {'post': post,
            # 'form': form,
            # 'comment_list': comment_list
            # }
    # return render(request, 'myblog/detail.html', context=context)

# def archives(request, year, month):
    # post_list = Post.objects.filter(created_time__year = year,
            # created_time__month = month)
    # return render(request, 'myblog/index.html', context = {'post_list': post_list})

# def category(request, pk):
    # cate = get_object_or_404(Category, pk = pk)
    # post_list = Post.objects.filter(category=cate)
    # return render(request, 'myblog/index.html', context = {'post_list': post_list})

class IndexView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = list(paginator.page_range)

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            
        data = {
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
                }
        return data


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year = self.kwargs.get('year'),
                created_time__month = self.kwargs.get('month'))

class PostDetailView(DetailView):
    model = Post
    template_name = 'myblog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions = [
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    TocExtension(slugify=slugify),
                    ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
            })
        return context

# def post_publish(request):
    # if request.method == "POST":
        # form = PostPublishForm(request.POST)
        
        # if form.is_valid():
            # post = form.save()
            # return redirect(post)
    # else:
        # form = PostPublishForm()
        # return render(request, 'myblog/post_publish.html', context = {'form': form})

# class PostPublishView(AdminRequiredMixin, FormView):
    # template_name = 'myblog/post_publish.html'
    # form_class = PostPublishForm
        
    # def get(self, request, *args, **kwargs):
        # form = self.form_class()
        # return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
            # post = form.save()
            # return redirect(post)
#         return render(request, self.template_name, {'form': form})

# def post_edit(request, pk):
    # post = get_object_or_404(Post, pk = pk)
    # if request.method == "POST":
        # form = PostPublishForm(request.POST)
        
        # if form.is_valid():
            # post.title = form.cleaned_data['title']
            # post.body = form.cleaned_data['body']
            # post.tags = form.cleaned_data['tags']
            # post.excerpt = form.cleaned_data['excerpt']
            # post.category = form.cleaned_data['category']
            # post.save()
            # return redirect(post)
    # else:
        # form = PostPublishForm(instance = post)
#         return render(request, 'myblog/post_publish.html', context = {'form': form})

class PostEditView(AdminRequiredMixin, UpdateView):
    model = Post
    template_name = 'myblog/post_publish.html'
    fields = ['title', 'body', 'tags', 'category', 'excerpt']

    def form_valid(self, form):
        clean = form.cleaned_data
        context = {}
        self.object = context.update(clean, force_update=True)
        return super(PostEditView, self).form_valid(form)
    
class PostPublishView(AdminRequiredMixin, CreateView):
    model = Post
    template_name = 'myblog/post_publish.html'
    fields = ['title', 'body', 'tags', 'category', 'excerpt']

    def form_valid(self, form):
        clean = form.cleaned_data
        form.instance.author=self.request.user
        context = {}
        self.object = context.update(clean, force_update=False)
        return super(PostPublishView, self).form_valid(form)

# class PostEditView(AdminRequiredMixin, FormView):
    # template_name = 'myblog/post_publish.html'
    # form_class = PostPublishForm

    # def get(self, request, *args, **kwargs):
        # post = get_object_or_404(Post, pk = self.kwargs.get('pk'))
        # form = self.form_class(instance = post)
        # return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
        # post = get_object_or_404(Post, pk = self.kwargs.get('pk'))
        # form = self.form_class(request.POST)
        # if form.is_valid():
            # post.title = form.cleaned_data['title']
            # post.body = form.cleaned_data['body']
            # post.tags = form.cleaned_data['tags']
            # post.excerpt = form.cleaned_data['excerpt']
            # post.category = form.cleaned_data['category']
            # post = form.save()
            # return redirect(post)

#         return render(request, self.template_name, {'form': form})


# class PostPublishView(FormView):
    # model = Post
    # template_name = 'myblog/post_publish.html'

    # def get_success_url(self):
        # post = get_object_or_404(Post, title = self.request.POST.get('title')).pk
        # success_url = reverse('myblog:detail', kwargs={'pk': post_pk})

    # def form_valid(self, form):
        # return super(PostPublishView, self).form_valid(form)

        # return success_url
