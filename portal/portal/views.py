from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'postlist.html'
    context_object_name = 'postlist'

class PostDetail(DetailView):
    model = Post
    template_name = 'postdetail.html'
    context_object_name = 'postdetail'
