from django.urls import path

from todo.views import auth_views, list_views, todo_views

urlpatterns = [
    path("", auth_views.home, name="home"),
    path("login/", auth_views.login, name="login"),
    path("logout/", auth_views.logout, name="logout"),
    path("callback/", auth_views.callback, name="callback"),
    path("todo/", todo_views.todo, name="todo"),
    path("todo/toggle/<int:todo_id>/", todo_views.toggle_todo, name="toggle_todo"),
    path("todo/delete/<int:todo_id>/", todo_views.delete_todo, name="delete_todo"),
    path("lists/create/", list_views.create_list, name="create_list"),
    path("lists/delete/<int:list_id>/", list_views.delete_list, name="delete_list"),
    path("lists/rename/<int:list_id>/", list_views.rename_list, name="rename_list"),
    path(
        "lists/<int:list_id>/add_todo/",
        list_views.add_todo_to_list,
        name="add_todo_to_list",
    ),
]
