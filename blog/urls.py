from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView 

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/approve_post/', views.post_approve, name='approve_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/new/save', views.publish_now, name='publish_now'),
    path('drafts', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/comment', views.add_comment_to_post, name='add_comment'),
    path('comment/<int:pk>/approve', views.approve_comment, name="approve_comment"),
    path('comment/<int:pk>/remove', views.remove_comment, name="remove_comment"),
    
]
