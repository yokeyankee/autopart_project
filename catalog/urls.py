from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.PartListView.as_view(), name='part_list'),
    path('part/<int:pk>/', views.PartDetailView.as_view(), name='part_detail'),
]