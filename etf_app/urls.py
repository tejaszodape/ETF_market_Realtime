from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/etf-data/', views.api_etf_data),
    path('api/commentary/', views.api_commentary),
    path('api/market-status/', views.api_market_status),
    path('api/sidebar-prices/', views.api_sidebar_prices),
]