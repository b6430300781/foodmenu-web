from django.urls import path
from .views import menu_list, login_view

urlpatterns = [
    path('menus/', menu_list),
    path('login/', login_view),
]