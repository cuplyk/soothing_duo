from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),

    # HTMX URLs
    path('like/<slug:slug>/', views.like_toggle, name='like_toggle'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/update/', views.comment_update, name='comment_update'),
    path('comment-item/<int:pk>/', views.comment_item, name='comment_item'),
]