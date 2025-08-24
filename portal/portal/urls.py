from django.urls import path
from .views import PostList, PostDetail, SearchPostList, NewsCreate, PostEdit, PostDelete, ArticleCreate, IndexView,\
logout_view, be_author, category_subscribe, category_unsubscribe, TestEmailView

urlpatterns = [
    path('postlist/', PostList.as_view(), name='post_list'),
    path('', IndexView.as_view(), name='post_list'),
    path('logout/', logout_view, name='logout'),
    path('be_author/', be_author, name='be_author'),
    path('postlist/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', SearchPostList.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('article/create/', ArticleCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('postlist/<str:category_name>', PostList.as_view(), name='posts_by_category'),
    path('postlist/subscribe_category/<str:category_name>', category_subscribe ,name='subscribe_category'),
    path('category_unsubscribe/<str:category_name>/', category_unsubscribe ,name='unsubscribe_category'),
    path('send_email_message', TestEmailView.as_view() ,name='send_email_message')
]