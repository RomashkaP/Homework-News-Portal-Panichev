from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

class TestEmailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'email_message.html', {})

    def post(self, request, *args, **kwargs):
        try:
            send_mail(
                subject='Проверяю переменную запроса, здесь все гуд!',
                message='Here message text',
                from_email='rilyultash@yandex.ru',
                recipient_list=[request.user.email, ],
                fail_silently=True
            )
            print(f"Письмо отправлено на rilyultash@yandex.ru")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
        return redirect('/send_email_message')

def category_subscribe(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    category.subscribers.add(request.user)
    return redirect('/postlist')

def category_unsubscribe(request, category_name):
    category = Category.objects.get(name=category_name)
    request.user.category_set.remove(category)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')

class IndexView (LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['user_categories'] = Category.objects.filter(subscribers=self.request.user)
        # Добавлю эквивалент верхней строчки для большего понимания связей многие ко многим
        # context['user_categories'] = self.request.user.category_set.all()
        return context

@login_required
def be_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class PostList(ListView):
    # model = Post
    template_name = 'postlist.html'
    context_object_name = 'postlist'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.kwargs.get('category_name')
        return context

    def get_queryset(self, **kwargs):
        category_name = self.kwargs.get('category_name')
        queryset = Post.objects.all()
        if category_name:
            queryset = Post.objects.filter(categoryes__name__iexact=category_name)
        return queryset.order_by('-time_in')

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
        post = form.save(commit=False)
        post.type = 'NW'
        # post.save()
        # form.save_m2m()
        # self.send_message(post)
        return super().form_valid(form)

    # def send_message(self, post):
    #     category = post.categoryes.first()
    #     subscribers = category.subscribers.all()
    #     for user in subscribers:
    #         html_content = render_to_string(
    #             'email_message.html',{
    #                 'post' : post,
    #                 'category' : category,
    #                 'user' : user
    #             }
    #         )
    #         msg = EmailMultiAlternatives(
    #             subject='Вот и отправка сообщения о новой записи, подписавшимся пользователям!',
    #             body='',
    #             from_email='rilyultash@yandex.ru',
    #             to=[user.email]
    #         )
    #         msg.attach_alternative(html_content, 'text/html')
    #         msg.send()

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class ArticleCreate (PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        # post.save()
        # form.save_m2m()
        # self.send_message(post)
        return super().form_valid(form)

    # def send_message(self, post):
    #     category = post.categoryes.first()
    #     subscribers = category.subscribers.all()
    #     for user in subscribers:
    #         html_content = render_to_string(
    #             'email_message.html',{
    #                 'post' : post,
    #                 'category' : category,
    #                 'user' : user
    #             }
    #         )
    #         msg = EmailMultiAlternatives(
    #             subject='Вот и отправка сообщения о новой записи, подписавшимся пользователям!',
    #             body='',
    #             from_email='rilyultash@yandex.ru',
    #             to=[user.email]
    #         )
    #         msg.attach_alternative(html_content, 'text/html')
    #         msg.send()

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

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