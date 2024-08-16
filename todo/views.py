import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from todo.models import Todo

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{
        settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def home(request):
    # Check if the user is authenticated by checking the session
    if request.session.get("user"):
        # Redirect authenticated users to the todo page
        return redirect(reverse("todo"))

    # Render the home page for unauthenticated users
    return render(
        request,
        "home.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


def login(request):
    # Check if the user is authenticated by checking the session
    if request.session.get("user"):
        # Redirect authenticated users to the todo page
        return redirect(reverse("todo"))

    # Proceed with the login process for unauthenticated users
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    userinfo = token.get("userinfo")

    # Store userinfo in the session
    request.session["user"] = json.dumps(userinfo)

    return redirect("todo")


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("home")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def todo(request):
    user = request.session.get("user")
    if not user:
        return redirect("home")

    # Ensure user is a dictionary
    if isinstance(user, str):
        user = json.loads(user)

    # Get the user ID from the correct location in the user dictionary
    userId = user.get("sub")  # or user.get("id_token", {}).get("sub")

    if request.method == "POST":
        task = request.POST.get("task")
        if task and userId:
            Todo.objects.create(task=task, user=userId)
        return redirect("todo")

    todos = Todo.objects.filter(user=userId)
    return render(request, "todo.html", context={"todos": todos})


def toggle_todo(request, todo_id):
    if request.method == "POST":
        todo = Todo.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
    return redirect("todo")


def delete_todo(request, todo_id):
    if request.method == "POST":
        Todo.objects.filter(id=todo_id).delete()
    return redirect("todo")
