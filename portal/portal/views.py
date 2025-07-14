from django.shortcuts import render
# from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'postlist.html'
    context_object_name = 'postlist'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'postdetail.html'
    context_object_name = 'postdetail'
