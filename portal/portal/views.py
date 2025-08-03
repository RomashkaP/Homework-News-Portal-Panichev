from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group



def logout_view(request):
    logout(request)
    return redirect('/')

class IndexView (LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def be_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'postlist.html'
    context_object_name = 'postlist'
    paginate_by = 10

class SearchPostList (ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'searchpost.html'
    context_object_name = 'searchpost'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'postdetail.html'
    context_object_name = 'postdetail'

class NewsCreate (PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'NW'
        return super().form_valid(form)

class ArticleCreate (PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'AR'
        return super().form_valid(form)

class PostEdit (LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('portal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete (PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')