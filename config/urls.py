from django.urls import path

from todo import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("todo/", views.todo, name="todo"),  # Add this line
]
