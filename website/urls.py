from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='signup'),

    path('dashboard', views.dashboard, name='dashboard'),

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

    path('zooadmission/view_zooadmission', views.view_zooadmission, name='view_zooadmission'),
    path('zooadmission/update_zooadmission/<int:zooadmission_id>', views.update_zooadmission, name='update_zooadmission'),
    
    path('attractions/view_attractions', views.view_attractions, name='view_attractions'),
    path('attractions/delete_attractions/<int:attractionsID>', views.delete_attractions, name='delete_attractions'),
    path('attractions/create_attractions', views.create_attractions, name='create_attractions'),
    path('attractions/sview_attractions/<int:attractions_id>', views.sview_attractions, name='sview_attractions'),
    
    path('buildings/view_buildings', views.view_buildings, name='view_buildings'),
    path('buildings/delete_buildings/<int:buildingsID>', views.delete_buildings, name='delete_buildings'),
    path('buildings/create_buildings', views.create_buildings, name='create_buildings'),
    path('buildings/update_buildings/<int:buildings_id>', views.update_buildings, name='update_buildings'),

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

    path('hourly_rate', views.hourly_rate, name="hourly_rate"),
    path('update_hourly_rate/<int:hID>', views.update_hourly_rate, name="update_hourly_rate"),

    path('daily_zoo_activity', views.daily_zoo_activity, name='daily_zoo_activity'),
    path('management_reporting', views.management_reporting, name='management_reporting'),
    path('animal_population', views.animal_population, name='animal_population'),
    path('top_attractions', views.top_attractions, name='top_attractions'),
]
