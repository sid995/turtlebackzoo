from django.contrib import messages
from django.db import connection, connections, IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from website.custom_func.custom_func import role_based_routing, dict_fetch_all


def home(request):
    print(request.session)
    # check_for_auth(request)
    return render(request, 'zoo/home.html', {'page_title': 'Home'})


def view_users(request):
    r = []
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        r = dict_fetch_all(cursor)
    return render(request, 'zoo/users/view_users.html', {'users': r})


def create_user(request):
    if request.method == 'POST':
        new_username = request.POST.get('newUsername')
        new_password = request.POST.get('newPassword')
        new_role = request.POST.get('new_role')

        query = "SELECT * FROM users WHERE Username = %s"
        cursor = connection.cursor()
        cursor.execute(query, [new_username])
        r = dict_fetch_all(cursor)

        if len(r) == 0:
            userinsertquery = "INSERT INTO users (Username, Password, Role) VALUES (%s, %s, %s)"
            try:
                with connections['default'].cursor() as cursor:
                    # execute query taking in username, password, role
                    cursor.execute(userinsertquery, [new_username, new_password, new_role])
            except IntegrityError as e:
                # Handle integrity constraint violations or other database errors
                print(f"Error executing raw SQL query: {e}")
                return False
            else:
                # Commit the changes if the query executed successfully
                connections['default'].commit()
                # redirect
                return redirect('/users/view_users')
        else:
            messages.error(request, 'Username already exists')
            return redirect('/users/create_user')
    return render(request, 'zoo/users/create_user.html')


def edit_user(request, username):
    if request.method == 'GET':
        getuserquery = "SELECT * FROM users WHERE Username='{}'".format(username)
        cursor = connection.cursor()
        cursor.execute(getuserquery)
        r = dict_fetch_all(cursor)
        if len(r) == 0:
            messages.error(request, 'User not found')
            return redirect('/users/view_users')
        else:
            return render(request, 'zoo/users/edit_user.html', {"userdata": r[0]})

    if request.method == 'POST':
        selected_user_role = request.POST.get('role')
        print(selected_user_role, username)
        edituserquery = "UPDATE users SET Role='{}' WHERE Username='{}'".format(selected_user_role, username)
        try:
            with connections['default'].cursor() as cursor:
                # execute query taking in username, password, role (default "User")
                cursor.execute(edituserquery)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            connections['default'].commit()
            # redirect
            return redirect('/users/view_users')


def delete_user(request, username):
    deleteuserquery = "DELETE FROM users WHERE Username='{}'".format(username)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(deleteuserquery)
    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        # Commit the changes if the query executed successfully
        connections['default'].commit()
        # redirect
        return redirect('/users/view_users')


def view_animals(request):
    viewanimalquery = """
        SELECT animal.ID, animal.Status, animal.BirthYear, species.Name AS SpeciesName, enclosure.ID AS EnclosureID, building.Name AS BuildingName
FROM animal
        LEFT JOIN species ON animal.SpeciesID = species.ID
        LEFT JOIN enclosure ON animal.EnclosureID = enclosure.ID
        LEFT JOIN building ON animal.BuildingID = building.ID;
    """
    cursor = connection.cursor()
    cursor.execute(viewanimalquery)
    r = dict_fetch_all(cursor)
    return render(request, 'zoo/animal/view_animals.html', {"animals": r})


def view_animal(request, animalID):
    return render(request, 'zoo/animal/view_animal.html', {"animals": 'r'})


def create_animal(request):
    if request.method == 'POST':
        status = request.POST['status']
        birthYear = request.POST['birthYear']
        speciesID = int(request.POST['species'])
        buildingID = int(request.POST['building'])
        enclosureID = int(request.POST['enclosure'])
        animalCreationQuery = "INSERT INTO animal (Status, BirthYear, SpeciesID, BuildingID, EnclosureID) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            status, birthYear, speciesID, buildingID, enclosureID)
        try:
            with connections['default'].cursor() as cursor:
                # execute query taking in username, password, role (default "User")
                cursor.execute(animalCreationQuery)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            connections['default'].commit()
            # redirect
            return redirect('/animals/view_animals')

    species_query = "SELECT * FROM species"
    building_query = "SELECT * FROM building"
    enclosure_query = "SELECT * FROM enclosure"

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(species_query)
            species_fetch = dict_fetch_all(cursor)
            cursor.execute(building_query)
            building_fetch = dict_fetch_all(cursor)
            cursor.execute(enclosure_query)
            enclosure_fetch = dict_fetch_all(cursor)
            print(species_fetch, building_fetch, enclosure_fetch)
    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        return render(request, 'zoo/animal/create_animal.html', {
            'species': species_fetch,
            'building': building_fetch,
            'enclosure': enclosure_fetch,

        })


def update_animal(request, animalID):
    if request.method == 'POST':
        newStatus = request.POST.get('status')
        newSpecies = request.POST.get('species')
        newBuilding = request.POST.get('building')
        newEnclosure = request.POST.get('enclosure')
        newBirthYear = request.POST.get('birthYear')
        print(type(int(newBuilding)), type(newBuilding))
        animalUpdateQuery = "UPDATE animal SET Status = '{}', BirthYear='{}', SpeciesID = '{}', BuildingID = '{}', EnclosureID = '{}' WHERE ID = '{}'".format(
            newStatus, newBirthYear, int(newSpecies), int(newBuilding), int(newEnclosure), animalID)

        try:
            with connections['default'].cursor() as cursor:
                # execute query taking in username, password, role (default "User")
                cursor.execute(animalUpdateQuery)

        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            connections['default'].commit()
            return redirect("/animals/view_animals")

    species_query = "SELECT * FROM species"
    building_query = "SELECT * FROM building"
    enclosure_query = "SELECT * FROM enclosure"

    animal_id_query = """
        SELECT a.ID, a.Status, a.BirthYear, a.SpeciesID, a.BuildingID, a.EnclosureID,
            s.Name AS SpeciesName, b.Name AS BuildingName, e.SqFt
            FROM animal a
            JOIN species s ON a.SpeciesID = s.ID
            JOIN building b ON a.BuildingID = b.ID
            JOIN enclosure e ON a.EnclosureID = e.ID
            WHERE a.ID = {} """.format(animalID)

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(species_query)
            species_fetch = dict_fetch_all(cursor)
            cursor.execute(building_query)
            building_fetch = dict_fetch_all(cursor)
            cursor.execute(enclosure_query)
            enclosure_fetch = dict_fetch_all(cursor)

            cursor.execute(animal_id_query)
            animal_fetch = dict_fetch_all(cursor)
            print(animal_fetch)
            if len(animal_fetch) != 1:
                return redirect("/animals/view_animals")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request, 'zoo/animal/update_animal.html', {
            'species': species_fetch,
            'building': building_fetch,
            'enclosure': enclosure_fetch,
            'animal': animal_fetch[0]
        })


def delete_animal(request, animalID):
    deleteanimalquery = "DELETE FROM animal WHERE ID = '{}'".format(animalID)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(deleteanimalquery)
    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        # Commit the changes if the query executed successfully
        connections['default'].commit()
        # redirect
        return redirect('/animals/view_animals')


def view_species(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM species")
    result = dict_fetch_all(cursor)
    return render(request, 'zoo/species/view_species.html', {'species': result})


def view_one_species(request, speciesID):
    cursor = connection.cursor()
    cursor.execute("SELECT ID, Name, FoodCost, updated_date FROM species WHERE ID = '{}'".format(speciesID))
    result = dict_fetch_all(cursor)
    print(result)
    if len(result) > 0:
        result = result[0]
        return render(request, 'zoo/species/view_one_species.html', {'species': result})
    else:
        return redirect('/species/view_species')


def create_species(request):
    if request.method == 'POST':
        name = request.POST['name']
        foodCost = request.POST['foodCost']
        create_species_query = "INSERT INTO species (Name, FoodCost, updated_date) VALUES ('{}', '{}', CURRENT_DATE)".format(
            name, foodCost)
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(create_species_query)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            connections['default'].commit()
            # redirect
            return redirect('/species/view_species')
    return render(request, 'zoo/species/create_species.html')


def update_species(request, species_id):
    if request.method == 'POST':
        name = request.POST['name']
        foodCost = request.POST['foodCost']
        update_species_query = "UPDATE species SET Name = '{}', FoodCost = '{}', updated_date = CURRENT_DATE WHERE ID = '{}'".format(name, foodCost, species_id)
        cursor = connection.cursor()
        try:
            cursor.execute(update_species_query)
        except IntegrityError as e:
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            connections['default'].commit()
            return redirect('/species/view_species')

    fetch_single_specie = "SELECT * FROM species WHERE ID = '{}'".format(species_id)

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(fetch_single_specie)
            species_fetch = dict_fetch_all(cursor)
            if len(species_fetch) != 1:
                return redirect("/species/view_species")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request, 'zoo/species/update_one_species.html', {
            'species': species_fetch[0]
        })


def delete_species(request, speciesID):
    delete_species_query = "DELETE FROM species WHERE ID = '{}'".format(speciesID)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(delete_species_query)
    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        # Commit the changes if the query executed successfully
        connections['default'].commit()
        # redirect
        return redirect('/species/view_species')

def view_zooadmission(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM zooadmission")
    result = dict_fetch_all(cursor)
    return render(request, 'zoo/zooadmission/view_zooadmission.html', {'zooadmission': result})

def update_zooadmission(request, zooadmission_id):
    if request.method == 'POST':
        SeniorPrice = request.POST.get('SeniorPrice')
        AdultPrice = request.POST.get('AdultPrice')
        ChildPrice = request.POST.get('ChildPrice')
        update_zooadmission_query = "UPDATE zooadmission SET SeniorPrice = '{}', AdultPrice = '{}', ChildPrice = '{}'".format(SeniorPrice, AdultPrice, ChildPrice, zooadmission_id)
        cursor = connection.cursor()
        try:
            cursor.execute(update_zooadmission_query)
        except IntegrityError as e:
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            connections['default'].commit()
            return redirect('/zooadmission/view_zooadmission')

    fetch_single_zooadmission = "SELECT * FROM zooadmission WHERE ID = '{}'".format(zooadmission_id)

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(fetch_single_zooadmission)
            zooadmission_fetch = dict_fetch_all(cursor)
            if len(zooadmission_fetch) != 1:
                return redirect("/zooadmission/view_zooadmission")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request, 'zoo/zooadmission/update_zooadmission.html', {
            'zooadmission': zooadmission_fetch[0]
        })

def view_attractions(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM animalshow")
    result = dict_fetch_all(cursor)
    return render(request, 'zoo/attractions/view_attractions.html', {'view_attractions': result})

def delete_attractions(request, attractionsID):
        delete_attractions_query = "DELETE FROM animalshow WHERE ID = '{}'".format(attractionsID)
        try:
            with connections['default'].cursor() as cursor:
              # execute query taking in username, password, role (default "User")
                cursor.execute( delete_attractions_query)
        except IntegrityError as e:
                # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
             # Commit the changes if the query executed successfully
             connections['default'].commit()
             return redirect('/attractions/view_attractions')
         
def create_attractions(request):
    if request.method == 'POST':
        ID = request.POST['ID']
        ShowsPerDay = request.POST['ShowsPerDay']
        SeniorPrice = request.POST['SeniorPrice']
        AdultPrice = request.POST['AdultPrice']
        ChildPrice = request.POST['ChildPrice']
        create_attractions_query = "INSERT INTO animalshow (ID ,ShowsPerDay, SeniorPrice, AdultPrice, ChildPrice) VALUES ('{}', '{}', '{}','{}','{}')".format(
           ID, ShowsPerDay, SeniorPrice, AdultPrice, ChildPrice)
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(create_attractions_query)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            connections['default'].commit()
            # redirect
            return redirect('/attractions/view_attractions')
    return render(request, 'zoo/attractions/create_attractions.html')

def sview_attractions(request, attractions_id):
    if request.method == 'POST':
        ID = request.POST.get('ID')
        ShowsPerDay = request.POST.get('ShowsPerDay')
        SeniorPrice = request.POST.get('SeniorPrice')
        AdultPrice = request.POST.get('AdultPrice')
        ChildPrice = request.POST.get('ChildPrice')
        update_attractions_query = "UPDATE animalshow SET ID = '{}', ShowsPerDay = '{}', SeniorPrice = '{}', AdultPrice = '{}', ChildPrice = '{}'".format( ID, ShowsPerDay,SeniorPrice, AdultPrice, ChildPrice, attractions_id)
        cursor = connection.cursor()
        try:
            cursor.execute(update_attractions_query)
        except IntegrityError as e:
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            connections['default'].commit()
            return redirect('/attractions/view_attractions')

    fetch_single_attractions = "SELECT * FROM animalshow WHERE ID = '{}'".format(attractions_id)

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(fetch_single_attractions)
            attractions_fetch = dict_fetch_all(cursor)
            if len(attractions_fetch) != 1:
                return redirect("/attractions/view_attractions")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request, 'zoo/attractions/sview_attractions.html', {
            'attractions': attractions_fetch[0]
        })





def asset_management(request):
    return render(request, 'zoo/asset_management.html', {'page_title': 'Asset Management'})


def daily_zoo_activity(request):
    return render(request, 'zoo/daily_zoo_activity.html', {'page_title': 'Daily Zoo Activity'})


def management_reporting(request):
    return render(request, 'zoo/management_reporting.html', {'page_title': 'Management Reporting'})


def animal_section(request):
    return render(request, 'zoo/animal/animal_section.html', {'page_title': 'Animals section'})


def building_section(request):
    return render(request, 'zoo/buildings/building_section.html', {'page_title': 'Building section'})


def attractions_section(request):
    return render(request, 'zoo/zoo_activity/attractions_section.html', {'page_title': 'Attractions section'})


def employee_section(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee")
    r = dict_fetch_all(cursor)
    return render(request,
                  'zoo/employee_section.html',
                  {'page_title': 'Employees section', 'data': r}
                  )


def employee_hwp(request):
    return render(request, 'zoo/employee_hwp.html', {'page_title': 'Employees hourly wage section'})


def animal_population(request):
    return render(request, 'zoo/animal/animal_population.html', {'page_title': 'Animal Population'})


def revenue_report(request):
    return render(request, 'zoo/revenue_report.html', {'page_title': 'Revenue Report'})


def attractions_activity(request):
    return render(request, 'zoo/zoo_activity/attractions_activity.html', {'page_title': 'Attractions Activity'})


def concessions_page(request):
    return render(request, 'zoo/zoo_activity/concessions_page.html', {'page_title': 'Concessions Page'})


def attendance_page(request):
    return render(request, 'zoo/zoo_activity/attendance_page.html', {'page_title': 'Attendance page'})


def top_attractions(request):
    return render(request, 'zoo/top_attractions.html', {'page_title': 'Top Attractions'})


def best_days(request):
    return render(request, 'zoo/best_days.html', {'page_title': 'Best Days'})


def avg_revenue(request):
    return render(request, 'zoo/avg_revenue.html', {'page_title': 'Average Revenue'})


def dashboard(request):
    return render(request, 'zoo/admin/dashboard.html', {'page_title': 'Dashboard'})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        query = "SELECT * FROM users WHERE Username = %s AND Password = %s"
        cursor = connection.cursor()
        cursor.execute(query, [username, password])
        results = dict_fetch_all(cursor)
        if len(results) > 0:
            request.session['username'] = results[0]['Username']
            request.session['role'] = results[0]['Role']
            role = request.session['role']
            route = role_based_routing(role)
            return redirect(route)
        else:
            return render(request,
                          'zoo/authentication/login.html',
                          {'page_title': 'Login', 'error': 'Invalid Username or Password'}
                          )
    else:
        return render(request, 'zoo/authentication/login.html', {'page_title': 'Login'})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmPassword']

        query = "SELECT * FROM users WHERE Username = %s"
        cursor = connection.cursor()
        cursor.execute(query, [username])
        r = dict_fetch_all(cursor)

        if len(r) > 0:
            return render(request, 'zoo/authentication/register.html',
                          {'page_title': 'Signup', 'error': 'Username already exists'})
        elif password != confirmpassword:
            return render(request, 'zoo/authentication/register.html',
                          {'page_title': 'Signup', 'error': 'Passwords do not match'})
        else:
            userinsertquery = "INSERT INTO users (Username, Password, Role) VALUES (%s, %s, %s)"
            try:
                with connections['default'].cursor() as cursor:
                    # execute query taking in username, password, role (default "User")
                    cursor.execute(userinsertquery, [username, password, "User"])
            except IntegrityError as e:
                # Handle integrity constraint violations or other database errors
                print(f"Error executing raw SQL query: {e}")
                return False
            else:
                # Commit the changes if the query executed successfully
                connections['default'].commit()
                # redirect
                return redirect('/login')

    return render(request, 'zoo/authentication/register.html', {'page_title': 'Signup'})


def logout(request):
    if 'username' in request.session or 'role' in request.session:
        del request.session['username']
        del request.session['role']
        request.session.modified = True
    return redirect(reverse('login'))
