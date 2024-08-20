import json

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from todo.models.list_model import List
from todo.models.todo_model import Todo


def todo(request):
    user = request.session.get("user")
    if not user:
        return redirect("home")

    # Ensure user is a dictionary
    if isinstance(user, str):
        user = json.loads(user)

    # Get the user ID from the correct location in the user dictionary
    userId = user.get("sub")  # or user.get("id_token", {}).get("sub")

    # Get all lists for the user
    lists = List.objects.filter(user=userId)

    # Get the current list
    current_list_id = request.GET.get("list_id")
    if current_list_id:
        current_list = get_object_or_404(List, id=current_list_id, user=userId)
        todos = Todo.objects.filter(list=current_list)
    else:
        current_list = None
        todos = []

    context = {
        "lists": lists,
        "current_list": current_list,
        "todos": todos,
    }
    return render(request, "todo.html", context=context)


def toggle_todo(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id)
        todo.completed = not todo.completed
        todo.save()
        return redirect(f"{reverse('todo')}?list_id={todo.list.id}")
    return redirect("todo")


def delete_todo(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id)
        list_id = todo.list.id
        todo.delete()
        return redirect(f"{reverse('todo')}?list_id={list_id}")
    return redirect("todo")
