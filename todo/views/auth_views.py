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
