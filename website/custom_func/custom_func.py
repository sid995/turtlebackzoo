import requests
from django.shortcuts import redirect


def role_based_routing(role):
    if role == 'Admin':
        route = "/dashboard"
    elif role == 'Manager':
        route = "/asset_management"
    else:
        route = "/"
    return route


def dict_fetch_all(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def check_for_auth(request):
    if 'username' not in request.session and 'role' not in request.session:
        return redirect("/login")
    else:
        return None
