from django.urls import path

from .views import IndexPageView, redirect_view


app_name = 'menu'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('menu/<slug:slug>/', redirect_view, name='details'),
]
