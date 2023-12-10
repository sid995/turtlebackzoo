from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('asset_management/', views.asset_management, name='asset_management'),
    path('daily_zoo_activity/', views.daily_zoo_activity, name='daily_zoo_activity'),
    path('management_reporting/', views.management_reporting, name='management_reporting'),
    path('animal_section/', views.animal_section, name='animal_section'),
    path('building_section/', views.building_section, name='building_section'),
    path('attractions_section/', views.attractions_section, name='attractions_section'),
    path('employee_section/', views.employee_section, name='employee_section'),
    path('employee_hwp/', views.employee_hwp, name='employee_hwp'),
    path('animal_population/', views.animal_population, name='animal_population'),
    path('revenue_report/', views.revenue_report, name='revenue_report'),
    path('attractions_activity/', views.attractions_activity, name='attractions_activity'),
    path('concessions_page/', views.concessions_page, name='concessions_page'),
    path('attendance_page/', views.attendance_page, name='attendance_page'),
    path('top_attractions/', views.top_attractions, name='top_attractions'),
    path('best_days/', views.best_days, name='best_days'),
    path('avg_revenue/', views.avg_revenue, name='avg_revenue'),
    path('login/', views.login, name='login'),
]