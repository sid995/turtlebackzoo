from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='signup'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('asset_management', views.asset_management, name='asset_management'),

    path('users/view_users', views.view_users, name='view_users'),
    path('users/create_user', views.create_user, name='view_users'),
    path('users/edit_user/<str:username>', views.edit_user, name='edit_user'),
    path('users/delete_user/<str:username>', views.delete_user, name='delete_user'),

    path('animals/view_animals', views.view_animals, name='view_animals'),
    path('animals/create_animal', views.create_animal, name='create_animal'),
    path('animals/update_animal/<int:animalID>', views.update_animal, name='update_animal'),
    path('animals/delete_animal/<int:animalID>', views.delete_animal, name='delete_animal'),

    path('species/view_species', views.view_species, name='view_species'),
    path('species/view_one_species/<int:speciesID>', views.view_one_species, name='view_one_species'),
    path('species/create_species', views.create_species, name='create_species'),
    path('species/update_species/<int:species_id>', views.update_species, name='update_species'),
    path('species/delete_species/<int:speciesID>', views.delete_species, name='delete_species'),

    path('employees/view_employees', views.view_employees, name='view_employees'),
    path('employees/create_employees', views.create_employees, name='create_employees'),
    path('employees/update_employees/<int:empId>', views.update_employees, name='update_employees'),
    path('employees/delete_employees/<int:empId>', views.delete_employees, name='delete_employees'),

    path('enclosures/view_enclosures', views.view_enclosures, name='view_enclosures'),
    path('enclosures/view_enclosure/<int:enId>', views.view_enclosure, name='view_enclosure'),
    path('enclosures/update_enclosure/<int:enId>', views.update_enclosure, name='update_enclosure'),
    path('enclosures/delete_enclosure/<int:enId>', views.delete_enclosure, name='delete_enclosure'),
    path('enclosures/create_enclosure', views.create_enclosure, name='create_enclosure'),

    path('concessions/view_concessions', views.view_concessions, name="view_concessions"),
    path('concessions/update_concessions/<int:conId>', views.update_concessions, name="update_concessions"),
    path('concessions/delete_concessions/<int:conId>', views.delete_concessions, name="delete_concessions"),
    path('concessions/create_concessions', views.create_concessions, name="create_concessions"),
    path('concessions/sales_concessions', views.sales_concessions, name="sales_concessions"),

    path('revenuetypes/view_revenuetypes', views.view_revenuetypes, name="view_revenuetypes"),
    path('revenuetypes/create_revenue_type', views.create_revenue_type, name="create_revenue_type"),
    path('revenuetypes/update_revenue_type/<int:revId>', views.update_revenue_type, name="update_revenue_type"),
    path('revenuetypes/delete_revenue_type/<int:revId>', views.delete_revenue_type, name="delete_revenue_type"),

    path('daily_zoo_activity', views.daily_zoo_activity, name='daily_zoo_activity'),
    path('management_reporting', views.management_reporting, name='management_reporting'),
    path('animal_section', views.animal_section, name='animal_section'),
    path('animal_population', views.animal_population, name='animal_population'),
    path('building_section', views.building_section, name='building_section'),
    path('attractions_section', views.attractions_section, name='attractions_section'),
    path('employee_section', views.employee_section, name='employee_section'),
    path('employee_hwp', views.employee_hwp, name='employee_hwp'),
    path('revenue_report', views.revenue_report, name='revenue_report'),
    path('attractions_activity', views.attractions_activity, name='attractions_activity'),
    path('concessions_page', views.concessions_page, name='concessions_page'),
    path('attendance_page', views.attendance_page, name='attendance_page'),
    path('top_attractions', views.top_attractions, name='top_attractions'),
    path('best_days', views.best_days, name='best_days'),
    path('avg_revenue', views.avg_revenue, name='avg_revenue'),
]
