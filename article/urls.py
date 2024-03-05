from django.urls import path
from .views import (
    article_list_view,
    article_detail_view,
    article_created_view,
    article_list_create_api_view
)

app_name = 'article'

urlpatterns = [
    path('list/', article_list_view, name='list'),
    path('detail/<int:pk>/', article_detail_view, name='detail'),
    path('create/', article_created_view, name='create'),
    path('list-create/', article_list_create_api_view, name='list-create')
]