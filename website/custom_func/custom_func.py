import requests
from django.shortcuts import redirect


def role_based_routing(role):
    return "/dashboard"


def dict_fetch_all(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
