from django.urls import path
from .views import PostList, PostDetail, SearchPostList, NewsCreate, PostEdit, PostDelete, ArticleCreate

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', SearchPostList.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('article/create/', ArticleCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]