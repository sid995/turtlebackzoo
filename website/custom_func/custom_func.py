import requests
from django.shortcuts import redirect


def role_based_routing(role):
    if role == 'Admin' or role == 'Manager':
        route = "/dashboard"
    else:
        route = "/"
    return route


def dict_fetch_all(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
