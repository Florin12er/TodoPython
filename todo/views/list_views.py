import json

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from todo.models.list_model import List
from todo.models.todo_model import Todo


def create_list(request):
    if request.method == "POST":
        user = request.session.get("user")
        if not user:
            return redirect("home")

        if isinstance(user, str):
            user = json.loads(user)

        userId = user.get("sub")
        list_name = request.POST.get("list_name")

        if list_name and userId:
            new_list = List.objects.create(name=list_name, user=userId)
            return redirect(f"{reverse('todo')}?list_id={new_list.id}")

    return redirect("todo")


# New function to rename a list


def rename_list(request, list_id):
    if request.method == "POST":
        list_to_rename = get_object_or_404(List, id=list_id)
        new_name = request.POST.get("new_name")
        if new_name:
            list_to_rename.name = new_name
            list_to_rename.save()
        return redirect(f"{reverse('todo')}?list_id={list_id}")
    return redirect("todo")


# New function to delete a list


def delete_list(request, list_id):
    if request.method == "POST":
        list_to_delete = get_object_or_404(List, id=list_id)
        list_to_delete.delete()
        return redirect("todo")
    return redirect("todo")


# New function to add a todo to a list


def add_todo_to_list(request, list_id):
    if request.method == "POST":
        user = request.session.get("user")
        if not user:
            return redirect("home")

        if isinstance(user, str):
            user = json.loads(user)

        userId = user.get("sub")
        task = request.POST.get("task")

        if task and userId:
            todo_list = get_object_or_404(List, id=list_id)
            Todo.objects.create(task=task, user=userId, list=todo_list)

        return redirect(f"{reverse('todo')}?list_id={list_id}")

    return redirect("todo")
