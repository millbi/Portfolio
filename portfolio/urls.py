from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('', index),
    path('index.html', index, name='index'),
    path('about.html', about),
    path('profile.html', profile),
    path('<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio-detail'),
    path('portfolio/new/', PortfolioCreateView.as_view(), name='portfolio-create'),
    path('create.html', create_portfolio, name='create'),
    path('portfolio/<int:pk>/update/', PortfolioUpdateView.as_view(), name='portfolio-update'),
    path('<int:pk>/add_likes/', views.AddLike.as_view(), name='add_likes'),
    path('<int:pk>/del_likes/', views.DelLike.as_view(), name='del_likes')
]
