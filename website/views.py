from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# Create your views here.
def home(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Employee")
    r = dictfetchall(cursor)
    print(r)
    print(connection.queries)
    return render(request, 'zoo/home.html', {'page_title': 'Home', 'data': r})


def asset_management(request):
    return render(request, 'zoo/asset_management.html', {'page_title': 'Asset Management'})


def daily_zoo_activity(request):
    return render(request, 'zoo/daily_zoo_activity.html', {'page_title': 'Daily Zoo Activity'})


def management_reporting(request):
    return render(request, 'zoo/management_reporting.html', {'page_title': 'Management Reporting'})


def animal_section(request):
    return render(request, 'zoo/animal_section.html', {'page_title': 'Animals section'})


def building_section(request):
    return render(request, 'zoo/building_section.html', {'page_title': 'Building section'})


def attractions_section(request):
    return render(request, 'zoo/attractions_section.html', {'page_title': 'Attractions section'})


def employee_section(request):
    return render(request, 'zoo/employee_section.html', {'page_title': 'Employees section'})


def employee_hwp(request):
    return render(request, 'zoo/employee_hwp.html', {'page_title': 'Employees hourly wage section'})


def animal_population(request):
    return render(request, 'zoo/animal_population.html', {'page_title': 'Animal Population'})


def revenue_report(request):
    return render(request, 'zoo/revenue_report.html', {'page_title': 'Revenue Report'})


def attractions_activity(request):
    return render(request, 'zoo/attractions_activity.html', {'page_title': 'Attractions Activity'})


def concessions_page(request):
    return render(request, 'zoo/concessions_page.html', {'page_title': 'Concessions Page'})


def attendance_page(request):
    return render(request, 'zoo/attendance_page.html', {'page_title': 'Attendance page'})


def top_attractions(request):
    return render(request, 'zoo/top_attractions.html', {'page_title': 'Top Attractions'})


def best_days(request):
    return render(request, 'zoo/best_days.html', {'page_title': 'Best Days'})


def avg_revenue(request):
    return render(request, 'zoo/avg_revenue.html', {'page_title': 'Average Revenue'})


def login(request):
    return render(request, 'zoo/login.html', {'page_title': 'Login'})
