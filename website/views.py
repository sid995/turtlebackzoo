from datetime import date

from django.contrib import messages
from django.db import connection, connections, IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from website.custom_func.custom_func import role_based_routing, dict_fetch_all

allowed_revenue_types = ['Animal Show', 'Concession', 'Zoo Admission']


def home(request):
    if 'username' not in request.session or 'role' not in request.session:
        return redirect("/login")
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
            user_insert_query = "INSERT INTO users (Username, Password, Role) VALUES (%s, %s, %s)"
            try:
                with connections['default'].cursor() as cursor:
                    # execute query taking in username, password, role
                    cursor.execute(user_insert_query, [new_username, new_password, new_role])
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
        get_user_query = "SELECT * FROM users WHERE Username='{}'".format(username)
        cursor = connection.cursor()
        cursor.execute(get_user_query)
        r = dict_fetch_all(cursor)
        if len(r) == 0:
            messages.error(request, 'User not found')
            return redirect('/users/view_users')
        else:
            return render(request, 'zoo/users/edit_user.html', {"userdata": r[0]})

    if request.method == 'POST':
        selected_user_role = request.POST.get('role')
        edit_user_query = "UPDATE users SET Role='{}' WHERE Username='{}'".format(selected_user_role, username)
        try:
            with connections['default'].cursor() as cursor:
                # execute query taking in username, password, role (default "User")
                cursor.execute(edit_user_query)
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
    delete_user_query = "DELETE FROM users WHERE Username='{}'".format(username)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(delete_user_query)
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
    view_animal_query = """
        SELECT animal.ID, animal.Status, animal.BirthYear, species.Name AS SpeciesName, enclosure.ID AS EnclosureID, building.Name AS BuildingName
FROM animal
        LEFT JOIN species ON animal.SpeciesID = species.ID
        LEFT JOIN enclosure ON animal.EnclosureID = enclosure.ID
        LEFT JOIN building ON animal.BuildingID = building.ID;
    """
    cursor = connection.cursor()
    cursor.execute(view_animal_query)
    r = dict_fetch_all(cursor)
    return render(request, 'zoo/animal/view_animals.html', {"animals": r})


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
    delete_animal_query = "DELETE FROM animal WHERE ID = '{}'".format(animalID)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(delete_animal_query)
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
        update_species_query = "UPDATE species SET Name = '{}', FoodCost = '{}', updated_date = CURRENT_DATE WHERE ID = '{}'".format(
            name, foodCost, species_id)
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
        update_zooadmission_query = "UPDATE zooadmission SET SeniorPrice = '{}', AdultPrice = '{}', ChildPrice = '{}'".format(
            SeniorPrice, AdultPrice, ChildPrice, zooadmission_id)
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
            cursor.execute(delete_attractions_query)
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
        update_attractions_query = "UPDATE animalshow SET ID = '{}', ShowsPerDay = '{}', SeniorPrice = '{}', AdultPrice = '{}', ChildPrice = '{}'".format(
            ID, ShowsPerDay, SeniorPrice, AdultPrice, ChildPrice, attractions_id)
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


def view_employees(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee")
    result = dict_fetch_all(cursor)
    return render(request, 'zoo/employees/view_employees.html', {'employees': result})


def create_employees(request):
    if request.method == 'POST':
        job_type = request.POST.get('jobType')
        first_name = request.POST.get('firstName')
        middle_name = request.POST.get('middleName')
        last_name = request.POST.get('lastName')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        ezip = request.POST.get('zip')
        super_id = request.POST.get('superID')
        hour_rate_id = request.POST.get('hourlyRateID')
        concession_id = request.POST.get('concessionID')
        zoo_admission_id = request.POST.get('zooAdmissionID')
        print(ezip, super_id, hour_rate_id, concession_id, zoo_admission_id)
        print(type(ezip), type(super_id), type(hour_rate_id), type(concession_id), type(zoo_admission_id))

        username = (first_name + ' ' + last_name).lower()
        # this is a temporary method.
        # can be enhanced later by adding some crypt or
        # implementing sha_256
        password = username
        startDate = date.today()

        create_employee_query = "INSERT INTO employee (StartDate, JobType, FirstName, MiddleName, LastName, Street, City, State, Zip, SuperID, HourlyRateID, ConcessionID, ZooAdmissionID) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            startDate, job_type, first_name, middle_name, last_name, street, city, state, ezip, int(float(super_id)),
            int(hour_rate_id), int(concession_id), int(zoo_admission_id))

        create_new_user_query = "INSERT INTO users (Username, Password, Role) VALUES ('{}', '{}', '{}')".format(
            username, password, job_type)

        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(create_employee_query)
                cursor.execute(create_new_user_query)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            print("Success")
            connections['default'].commit()
            # redirect
            return redirect('/employees/view_employees')

    employee_query = "SELECT EmployeeID, CONCAT(FirstName, ' ', LastName) AS FullName FROM employee"
    hour_rate_query = "SELECT ID, HourlyRate FROM hourlyrate"
    concession_query = "SELECT ID, Product FROM concession"
    zoo_admission_query = "SELECT ID FROM zooadmission"

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(employee_query)
            employees_fetch = dict_fetch_all(cursor)
            cursor.execute(hour_rate_query)
            hour_rate_fetch = dict_fetch_all(cursor)
            cursor.execute(concession_query)
            concession_fetch = dict_fetch_all(cursor)
            cursor.execute(zoo_admission_query)
            zoo_admission_fetch = dict_fetch_all(cursor)

            if len(employees_fetch) == 0:
                return redirect("/employees/view_employees")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request,
                      'zoo/employees/create_employees.html',
                      {
                          'employees': employees_fetch,
                          'hour_rate': hour_rate_fetch,
                          'concession': concession_fetch,
                          'zoo_admission': zoo_admission_fetch
                      })


def update_employees(request, empId):
    if request.method == 'GET':
        employee_query = "SELECT EmployeeID, FirstName, MiddleName, LastName, StartDate, JobType, CONCAT(FirstName, ' ', LastName) AS FullName FROM employee WHERE EmployeeID='{}'".format(
            empId)
        cursor = connection.cursor()
        cursor.execute(employee_query)
        r = dict_fetch_all(cursor)

        if len(r) == 0:
            return redirect("/employees/view_employees")
        print(r)
        return render(request,
                      'zoo/employees/update_employees.html',
                      {'employee': r[0]}
                      )

    if request.method == "POST":
        job_type = request.POST.get('newJobType')
        start_date = request.POST.get('newStartDate')
        first_name = request.POST.get('newFirstName')
        middle_name = request.POST.get('newMiddleName')
        last_name = request.POST.get('newLastName')

        if request.session['role'] == "Admin":
            update_sql = "UPDATE employee SET StartDate = '{}', JobType = '{}', FirstName = '{}', MiddleName = '{}', LastName = '{}' WHERE EmployeeID = '{}'".format(
                start_date, job_type, first_name, middle_name, last_name, empId)
            cursor = connection.cursor()
            cursor.execute(update_sql)
            connections['default'].commit()
            # redirect
            return redirect('/employees/view_employees')


def delete_employees(request, empId):
    delete_query = "DELETE FROM employee WHERE EmployeeID = '{}'".format(empId)
    cursor = connection.cursor()
    cursor.execute(delete_query)
    connections['default'].commit()
    # redirect
    return redirect('/employees/view_employees')


def view_enclosures(request):
    enclosure_query = "SELECT e.ID, e.SqFt, b.Name AS BuildingName FROM enclosure e JOIN building b ON e.BuildingID = b.ID"
    cursor = connection.cursor()
    cursor.execute(enclosure_query)
    r = dict_fetch_all(cursor)
    # redirect
    return render(request,
                  'zoo/enclosures/view_enclosures.html',
                  {'enclosures': r}
                  )


def view_enclosure(request, enId):
    enclosure_query = "SELECT e.ID, e.SqFt, b.Name AS BuildingName FROM enclosure e JOIN building b ON e.BuildingID = b.ID WHERE e.ID = '{}'".format(
        enId)
    cursor = connection.cursor()
    cursor.execute(enclosure_query)
    r = dict_fetch_all(cursor)
    return render(request, 'zoo/enclosures/view_enclosure.html', {"enclosure": r[0]})


def update_enclosure(request, enId):
    if request.method == "POST":
        buildingId = request.POST.get('buildingId')
        sqft = request.POST.get('sqFt')
        update_enclosure_query = "UPDATE enclosure SET BuildingID = '{}', SqFt = '{}' WHERE ID = '{}'".format(
            buildingId, sqft, enId)
        cursor = connection.cursor()
        cursor.execute(update_enclosure_query)
        connections['default'].commit()
        return redirect('/enclosures/view_enclosures')

    enclosure_query = "SELECT BuildingID, SqFt FROM enclosure WHERE ID = '{}'".format(enId)
    cursor = connection.cursor()
    cursor.execute(enclosure_query)
    r = dict_fetch_all(cursor)

    get_buildings = "SELECT ID, Name FROM building"
    cursor = connection.cursor()
    cursor.execute(get_buildings)
    b = dict_fetch_all(cursor)
    print(r, b)
    return render(request, 'zoo/enclosures/update_enclosure.html', {"enclosure": r[0], "buildings": b})


def delete_enclosure(request, enId):
    delete_query = "DELETE FROM enclosure WHERE ID = '{}'".format(enId)
    cursor = connection.cursor()
    cursor.execute(delete_query)
    connections['default'].commit()
    return redirect('/enclosures/view_enclosures')


def create_enclosure(request):
    if request.method == 'POST':
        buildingId = request.POST.get('buildingId')
        sqft = request.POST.get('sqFt')
        create_enclosure_query = "INSERT INTO enclosure (BuildingID, SqFt) VALUES ('{}', '{}')".format(buildingId, sqft)
        cursor = connection.cursor()
        cursor.execute(create_enclosure_query)
        connections['default'].commit()
        return redirect('/enclosures/view_enclosures')

    fetch_building = "SELECT ID, Name FROM building"
    cursor = connection.cursor()
    cursor.execute(fetch_building)
    r = dict_fetch_all(cursor)
    return render(request, 'zoo/enclosures/create_enclosure.html', {"buildings": r})


def view_concessions(request):
    concessions_query = "SELECT C.ID, RT.Name AS RevenueType, C.Product FROM concession AS C JOIN revenuetype AS RT ON C.ID = RT.ID"
    cursor = connection.cursor()
    cursor.execute(concessions_query)
    r = dict_fetch_all(cursor)

    return render(request, 'zoo/concessions/view_concessions.html', {"concessions": r})


def update_concessions(request, conId):
    if request.method == "POST":
        productName = request.POST.get('updatedProduct')
        update_query = "UPDATE concession SET Product = '{}' WHERE ID = '{}'".format(productName, conId)
        cursor = connection.cursor()
        cursor.execute(update_query)
        connections['default'].commit()
        return redirect('/concessions/view_concessions')

    concession_query = "SELECT C.ID, RT.Name AS RevenueType, C.Product FROM concession AS C JOIN revenuetype AS RT ON C.ID = RT.ID WHERE C.ID = '{}'".format(
        conId)
    cursor = connection.cursor()
    cursor.execute(concession_query)
    r = dict_fetch_all(cursor)

    return render(request, 'zoo/concessions/update_concessions.html', {"concessions": r[0]})


def delete_concessions(request, conId):
    concession_query = "DELETE FROM concession WHERE ID = '{}'".format(conId)
    cursor = connection.cursor()
    cursor.execute(concession_query)
    connections['default'].commit()
    return redirect('/concessions/view_concessions')


def create_concessions(request):
    if request.method == "POST":
        revenueId = request.POST.get('revenueTypeId')
        productName = request.POST.get('product')
        update_query = "INSERT INTO concession (ID, Product) VALUES ('{}', '{}')".format(revenueId, productName)
        cursor = connection.cursor()
        cursor.execute(update_query)
        connections['default'].commit()
        return redirect('/concessions/view_concessions')

    fetch_revenue = "SELECT ID, Name FROM revenuetype"
    cursor = connection.cursor()
    cursor.execute(fetch_revenue)
    r = dict_fetch_all(cursor)
    return render(request, 'zoo/concessions/create_concessions.html', {"revenue_type": r})


def sales_concessions(request):
    if request.method == "POST":
        concessionID = request.POST.get('concessionID')
        concessionName = request.POST.get('concessionName')
        daily_concession_revenue = "INSERT INTO dailyconcessionrevenue (ConcessionID, Revenue) VALUES ('{}', '{}')".format(
            concessionID, concessionName)
        cursor = connection.cursor()
        cursor.execute(daily_concession_revenue)
        connections['default'].commit()
        return redirect('/concessions/view_concessions')

    daily_concession_query = "SELECT RecordID, Product, Revenue, SaleDate FROM dailyconcessionrevenue JOIN concession ON dailyconcessionrevenue.ConcessionID = concession.ID"

    cursor = connection.cursor()
    cursor.execute(daily_concession_query)
    r = dict_fetch_all(cursor)

    concession_query = "SELECT ID, Product FROM concession"
    cursor.execute(concession_query)
    c = dict_fetch_all(cursor)
    return render(request, 'zoo/concessions/sales_concession.html', {"daily_concession": r, "concessions": c})


def view_revenuetypes(request):
    revenue_query = "SELECT revenuetype.ID, revenuetype.Name, revenuetype.Type, building.Name AS BuildingName FROM revenuetype LEFT JOIN building ON revenuetype.BuildingID = building.ID"
    cursor = connection.cursor()
    cursor.execute(revenue_query)
    r = dict_fetch_all(cursor)

    return render(request, 'zoo/revenue_type/view_revenue_types.html', {"revenue_types": r})


def create_revenue_type(request):
    if request.method == 'POST':
        productName = request.POST.get('name')
        productType = request.POST.get('type')
        buildingId = request.POST.get('buildingId')

        revenue_create_query = "INSERT INTO revenuetype (Name, Type, BuildingID) VALUES ('{}', '{}', '{}')".format(
            productName, productType, buildingId)
        cursor = connection.cursor()
        cursor.execute(revenue_create_query)
        connections['default'].commit()
        return redirect('/revenuetypes/view_revenuetypes')

    building_query = "SELECT ID, Name FROM building"
    cursor = connection.cursor()
    cursor.execute(building_query)
    r = dict_fetch_all(cursor)

    return render(request, 'zoo/revenue_type/create_revenue_type.html',
                  {"buildings": r, "allowed_revenue_types": allowed_revenue_types})


def update_revenue_type(request, revId):
    if request.method == 'POST':
        productName = request.POST.get('name')
        productType = request.POST.get('type')
        buildingId = request.POST.get('buildingId')

        update_query = "UPDATE revenuetype SET Name = '{}', Type = '{}', BuildingID = '{}' WHERE ID = '{}'".format(
            productName, productType, buildingId, revId)
        cursor = connection.cursor()
        cursor.execute(update_query)
        connections['default'].commit()
        return redirect('/revenuetypes/view_revenuetypes')

    revenue_query = "SELECT * FROM revenuetype WHERE ID = '{}'".format(revId)
    building_query = "SELECT ID, Name FROM building"

    cursor = connection.cursor()
    cursor.execute(revenue_query)
    r = dict_fetch_all(cursor)
    cursor.execute(building_query)
    b = dict_fetch_all(cursor)
    return render(request, 'zoo/revenue_type/update_revenue_file.html',
                  {"revenueType": r[0], "allowed_revenue_types": allowed_revenue_types, "buildings": b})


def delete_revenue_type(request, revId):
    delete_query = "DELETE FROM revenuetype WHERE ID = '{}'".format(revId)
    cursor = connection.cursor()
    cursor.execute(delete_query)
    connections['default'].commit()
    # redirect
    return redirect('/revenuetypes/view_revenuetypes')


def daily_zoo_activity(request):
    return render(request, 'zoo/daily_zoo_activity.html', {'page_title': 'Daily Zoo Activity'})


def management_reporting(request):
    return render(request, 'zoo/management_reporting.html', {'page_title': 'Management Reporting'})


def animal_population(request):
    r = []
    if request.method == "POST":
        month = request.POST['selectedMonth']
        report_query = "SELECT animal.SpeciesID, species.Name AS SpeciesName, animal.Status, SUM(species.FoodCost) AS TotalFoodCost, SUM(hourlyrate.HourlyRate * 40) AS TotalLaborCost FROM animal INNER JOIN species ON animal.SpeciesID = species.ID LEFT JOIN caresfor ON animal.SpeciesID = caresfor.SpeciesID LEFT JOIN employee ON caresfor.EmployeeID = employee.EmployeeID LEFT JOIN hourlyrate ON employee.HourlyRateID = hourlyrate.ID WHERE DATE_FORMAT(species.updated_date, '%Y-%m') = '{}' GROUP BY animal.SpeciesID, animal.Status".format(
            month)
        cursor = connection.cursor()
        cursor.execute(report_query)
        r = dict_fetch_all(cursor)

    return render(request, 'zoo/animalPopulationReport/animal-population-report.html', {'report': r})


def top_attractions(request):
    r = []
    startDate = None
    endDate = None
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']

        query = """SELECT
                    AnimalShowID,
                    SUM(Revenue) AS TotalRevenue
                    FROM animalshowtickets
                    WHERE CheckoutTime BETWEEN '{}' AND '{}'
                    GROUP BY AnimalShowID
                    ORDER BY TotalRevenue DESC
                    LIMIT 3
        """.format(startDate, endDate)

        cursor = connection.cursor()
        cursor.execute(query)
        r = dict_fetch_all(cursor)
    return render(request, 'zoo/top_attractions.html', {"result": r, "startDate": startDate, "endDate": endDate})


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
        confirm_password = request.POST['confirmPassword']

        query = "SELECT * FROM users WHERE Username = %s"
        cursor = connection.cursor()
        cursor.execute(query, [username])
        r = dict_fetch_all(cursor)

        if len(r) > 0:
            return render(request, 'zoo/authentication/register.html',
                          {'page_title': 'Signup', 'error': 'Username already exists'})
        elif password != confirm_password:
            return render(request, 'zoo/authentication/register.html',
                          {'page_title': 'Signup', 'error': 'Passwords do not match'})
        else:
            user_insert_query = "INSERT INTO users (Username, Password, Role) VALUES (%s, %s, %s)"
            try:
                with connections['default'].cursor() as cursor:
                    # execute query taking in username, password, role (default "User")
                    cursor.execute(user_insert_query, [username, password, "User"])
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


def hourly_rate(request):
    rate_query = "SELECT * FROM hourlyrate"
    cursor = connection.cursor()
    cursor.execute(rate_query)
    result = dict_fetch_all(cursor)
    print(result)

    return render(request, 'zoo/hourlyRate/hourly_rate.html', {"result": result})


def update_hourly_rate(request, hID):
    if request.method == 'POST':
        newHourlyRate = request.POST['newHourlyRate']
        update_query = "UPDATE hourlyrate SET HourlyRate = '{}' WHERE ID = '{}'".format(newHourlyRate, hID)
        cursor = connection.cursor()
        cursor.execute(update_query)
        connections['default'].commit()
        # redirect
        return redirect('/hourly_rate')

    hourly_query = "SELECT * FROM hourlyrate WHERE ID = '{}'".format(hID)
    cursor = connection.cursor()
    cursor.execute(hourly_query)
    result = dict_fetch_all(cursor)

    if len(result) == 0:
        return redirect('/hourly_rate')

    return render(request, "zoo/hourlyRate/update_hourly_rate.html", {"result": result[0], "hID": hID})


def view_buildings(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM building")
    result = dict_fetch_all(cursor)
    return render(request, 'zoo/buildings/view_buildings.html', {'view_buildings': result})


def delete_buildings(request, buildingsID):
    delete_buildings_query = "DELETE FROM building WHERE ID = '{}'".format(buildingsID)
    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(delete_buildings_query)
    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        # Commit the changes if the query executed successfully
        connections['default'].commit()
        return redirect('/buildings/view_buildings')


def create_buildings(request):
    if request.method == 'POST':
        ID = request.POST['ID']
        Name = request.POST['Name']
        Type = request.POST['Type']

        create_buildings_query = "INSERT INTO building (ID ,Name, Type) VALUES ('{}', '{}', '{}')".format(
            ID, Name, Type)
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(create_buildings_query)
        except IntegrityError as e:
            # Handle integrity constraint violations or other database errors
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            # Commit the changes if the query executed successfully
            connections['default'].commit()
            # redirect
            return redirect('/buildings/view_buildings')
    return render(request, 'zoo/buildings/create_buildings.html')


def update_buildings(request, buildings_id):
    if request.method == 'POST':
        ID = request.POST.get('ID')
        Name = request.POST.get('Name')
        Type = request.POST.get('Type')
        update_buildings_query = "UPDATE building SET ID = '{}', Name = '{}', Type = '{}'".format(ID, Name, Type,
                                                                                                  buildings_id)
        cursor = connection.cursor()
        try:
            cursor.execute(update_buildings_query)
        except IntegrityError as e:
            print(f"Error executing raw SQL query: {e}")
            return False
        else:
            connections['default'].commit()
            return redirect('/buildings/view_buildings')

    fetch_single_buildings = "SELECT * FROM building WHERE ID = '{}'".format(buildings_id)

    try:
        with connections['default'].cursor() as cursor:
            # execute query taking in username, password, role (default "User")
            cursor.execute(fetch_single_buildings)
            buildings_fetch = dict_fetch_all(cursor)
            if len(buildings_fetch) != 1:
                return redirect("/buildings/view_buildings")

    except IntegrityError as e:
        # Handle integrity constraint violations or other database errors
        print(f"Error executing raw SQL query: {e}")
        return False
    else:
        connections['default'].commit()
        return render(request, 'zoo/buildings/update_buildings.html', {
            'buildings': buildings_fetch[0]
        })
