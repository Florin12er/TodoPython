import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

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
    print(
        f"Home view accessed. User authenticated: {
            request.user.is_authenticated}"
    )
    return render(request, "home.html")


# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("todo")))


# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def todo(request):
    return render(request, "todo.html")
