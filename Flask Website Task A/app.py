"""
Task A

Written by Ching Loo s3557584
app.py

This file mainly has the code for the routes of the flask application.
"""
from flask import Flask, render_template, request, session, url_for, flash, redirect, abort
from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.validators import InputRequired
from requestsUtil import requestsUtil
from pushbullet import PushBullet

app = Flask(__name__)


@app.route('/')
def index():
    """
    Route for Index page of the website

    Parameters:
        None

    Returns:
       render_template('home.html'): Renders html template for the index page of the website
    """
    return render_template('home.html')


class Login(Form):
    """
    Login Class

    A form type class handles the input validation for login
    """
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for Admin login page of the website.

    Parameters:
        None

    Returns:
        render_template('login.html', form=form): Renders the HTML login page
    """
    obj = requestsUtil()
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password_candidate = form.password.data

        results = obj.get_admin(username)
        status = not bool(results)

        if status != True:

            decryptedPassword = obj.decryptPassword(
                results.get("adminPassword"))

            if decryptedPassword == password_candidate:
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Password incorrect!!!"
                return render_template('login.html', error=error, form=form)
        else:
            error = "Username incorrect!!!"
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)


@app.route('/login_engineer', methods=['GET', 'POST'])
def login_engineer():
    """
    Route for Engineer login page of the website.

    Parameters:
        None

    Returns:
        render_template('login.html', form=form): Renders the HTML login page
    """
    obj = requestsUtil()
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password_candidate = form.password.data

        results = obj.get_engineer(username)
        status = not bool(results)

        if status != True:

            decryptedPassword = obj.decryptPassword(
                results.get("engineerPassword"))

            if decryptedPassword == password_candidate:
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('vehicle_locations'))
            else:
                error = "Password incorrect!!!"
                return render_template('login.html', error=error, form=form)
        else:
            error = "Username incorrect!!!"
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)


@app.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    """
    Route for Manager login page of the website.

    Parameters:
        None

    Returns:
        render_template('login.html', form=form): Renders the HTML login page 
    """
    obj = requestsUtil()
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password_candidate = form.password.data

        results = obj.get_manager(username)
        status = not bool(results)

        if status != True:

            decryptedPassword = obj.decryptPassword(
                results.get("managerPassword"))

            if decryptedPassword == password_candidate:
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('manager_dashboard'))
            else:
                error = "Password incorrect!!!"
                return render_template('login.html', error=error, form=form)
        else:
            error = "Username incorrect!!!"
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)

# Check if user logged in


def is_logged_in(f):
    """
    A function to check if the current user is still logged in to the website
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
def logout():
    """
    Route for logout.

    Parameters:
        None

    Returns:
        redirect(url_for('index')): Redirects the user back to the index page after logging out.
    """
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    """
    Route for dashboard page of the website

    Parameters:
        None

    Returns:
       render_template('home.html'): Renders html template for the admin dashboard page of the website
    """
    return render_template('dashboard.html')


class UserForm(Form):
    """
    UserForm Class

    A form type class handles the input validation for add user
    """
    username = StringField('Username', [validators.length(min=1, max=50)])
    firstname = StringField('First Name', [validators.length(min=1, max=50)])
    surname = StringField('Surname', [validators.length(min=1, max=50)])
    password = StringField('Password', [validators.length(min=1, max=50)])
    imageName = StringField('Image Name', [validators.length(min=1, max=50)])


@app.route('/add_user', methods=['GET', 'POST'])
@is_logged_in
def add_user():
    """
    Route for add user page of the website

    Parameters:
        None

    Returns:
       return redirect(url_for('dashboard')): Redirects to the dashboard page
       return render_template('add_user.html', form=form): Render the add user HTML page
    """
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        firstname = form.firstname.data
        surname = form.surname.data
        password = form.password.data
        imageName = form.imageName.data

        obj = requestsUtil()

        encryptedPassword = obj.encryptPassword(password)

        obj.add_user(username, firstname, surname,
                     encryptedPassword, imageName)

        flash('User Added', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_user.html', form=form)


@app.route('/edit_user/<string:userID>', methods=['GET', 'POST'])
@is_logged_in
def edit_user(userID):
    """
    Route for edit user page of the website

    Parameters:
        userID(Integer): User ID from database

    Returns:
       return redirect(url_for('dashboard')): Redirects to the dashboard page
       return render_template('edit_user.html', form=form): Render the edit user HTML page
    """
    obj = requestsUtil()
    result = obj.get_user(userID)

    form = UserForm(request.form)

    decryptedPassword = obj.decryptPassword(result['password'])

    form.username.data = result['username']
    form.firstname.data = result['firstname']
    form.surname.data = result['surname']
    form.password.data = decryptedPassword
    form.imageName.data = result['imageName']

    if request.method == 'POST' and form.validate():
        username = request.form['username']
        firstname = request.form['firstname']
        surname = request.form['surname']
        password = request.form['password']
        imageName = request.form['imageName']

        encryptedPassword = obj.encryptPassword(password)

        obj = requestsUtil()
        obj.update_user(userID, username, firstname, surname,
                        encryptedPassword, imageName)

        flash('User Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_user.html', form=form)


class VehicleForm(Form):
    brand = StringField('Brand', [validators.length(min=1, max=50)])
    colour = StringField('Colour', [validators.length(min=1, max=50)])
    cost = SelectField(
        'Cost', choices=[("15", "15"), ("20", "20"), ("25", "25")])
    seats = SelectField('Seats', choices=[("2", "2"), ("4", "4"), ("7", "7")])
    model = StringField('Model', [validators.length(min=1, max=50)])


@app.route('/add_vehicle', methods=['GET', 'POST'])
@is_logged_in
def add_vehicle():
    """
    Route for add vehicle page of the website

    Parameters:
        None

    Returns:
       return redirect(url_for('dashboard')): Redirects to the dashboard page
       return render_template('add_vehicle.html', form=form): Render the add vehicle HTML page
    """
    form = VehicleForm(request.form)
    if request.method == 'POST' and form.validate():
        brand = form.brand.data
        colour = form.colour.data
        cost = form.cost.data
        seats = form.seats.data
        model = form.model.data

        obj = requestsUtil()
        obj.add_vehicle(brand, colour, cost, seats, model)

        flash('Vehicle Added', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_vehicle.html', form=form)


@app.route('/edit_vehicle/<string:vehicleID>', methods=['GET', 'POST'])
@is_logged_in
def edit_vehicle(vehicleID):
    """
    Route for edit user page of the website

    Parameters:
        vehicleID(Integer): Vehicle ID from the database

    Returns:
       return redirect(url_for('dashboard')): Redirects to the dashboard page
       return render_template('edit_vehicle.html', form=form): Render the edit vehicle HTML page
    """
    obj = requestsUtil()
    result = obj.get_vehicle(vehicleID)

    form = VehicleForm(request.form)

    form.brand.data = result['vehicleBrand']
    form.colour.data = result['colour']
    form.model.data = result['vehicleModel']

    if request.method == 'POST' and form.validate():
        vehicleBrand = request.form['brand']
        colour = request.form['colour']
        cost = request.form['cost']
        seats = request.form['seats']
        vehicleModel = request.form['model']

        obj = requestsUtil()
        obj.update_vehicle(vehicleID, vehicleBrand, colour,
                           cost, seats, vehicleModel)

        flash('Vehicle Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_vehicle.html', form=form)


class SearchUser(Form):
    """
    SearchUser Form Class

    A form type class handles the input validation for search user
    """
    category = SelectField('Catergory', choices=[(
        "username", "Username"), ("firstname", "First Name"), ("surname", "Surname")])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])


@app.route('/search_user', methods=['GET', 'POST'])
@is_logged_in
def searchUser():
    """
    Route for search user page of the website

    Parameters:
       None

    Returns:
       return render_template('searchUser.html', data=data, form=form, error=error): Render the search user HTML page
    """
    form = SearchUser(request.form)
    objRec = requestsUtil()
    if request.method == "POST" and form.validate():
        keyword = form.keyword.data
        category = form.category.data
        results = objRec.get_users()
        data = objRec.search(keyword, category, results)
        if not data:
            error = 'No Result!!!'
            return render_template('searchUser.html', data=data, form=form, error=error)
        else:
            return render_template('searchUser.html', data=data, form=form)

    return render_template('searchUser.html', form=form)


class SearchVehicle(Form):
    """
    SearchVehicle Form Class

    A form type class handles the input validation for search Vehicle
    """
    category = SelectField('Catergory', choices=[(
        'colour', 'Colour'), ('vehicleBrand', 'Brand'), ('vehicleModel', 'Model')])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])


@app.route('/search_vehicle', methods=['GET', 'POST'])
@is_logged_in
def searchVehicle():
    """
    Route for search vehicle page of the website

    Parameters:
       None

    Returns:
       return render_template('searchVehicle.html', data=data, form=form, error=error): Render the search vehicle HTML page
    """
    form = SearchVehicle(request.form)
    objRec = requestsUtil()
    if request.method == "POST" and form.validate():
        keyword = form.keyword.data
        category = form.category.data
        results = objRec.get_vehicles()
        data = objRec.search(keyword, category, results)
        if not data:
            error = 'No Result!!!'
            return render_template('searchVehicle.html', data=data, form=form, error=error)
        else:
            return render_template('searchVehicle.html', data=data, form=form)

    return render_template('searchVehicle.html', form=form)


@app.route('/delete_vehicle/<string:vehicleID>', methods=['GET', 'POST'])
@is_logged_in
def deleteVehicle(vehicleID):
    """
    Route for delete vehicle page of the website

    Parameters:
       vehicleID(Integer): Vehicle ID from database.

    Returns:
       return redirect(url_for('dashboard')): Redirect to Admin dashboard page
    """
    obj = requestsUtil()
    obj.delete_vehicle(vehicleID)

    flash('Vehicle Deleted', 'success')

    return redirect(url_for('dashboard'))


@app.route('/delete_user/<string:userID>', methods=['GET', 'POST'])
@is_logged_in
def deleteUser(userID):
    """
    Route for delete user page of the website

    Parameters:
       userID(Integer): User ID from database.

    Returns:
       return redirect(url_for('dashboard')): Redirect to Admin dashboard page
    """
    obj = requestsUtil()
    obj.delete_user(userID)

    flash('User Deleted', 'success')

    return redirect(url_for('dashboard'))


class MaintenanceForm(Form):
    """
    MaintenanceForm Class

    A form type class handles the input validation for report vehicle page
    """
    engineerName = SelectField('Engineer')


@app.route('/report_vehicle/<string:vehicleID>', methods=['GET', 'POST'])
@is_logged_in
def add_maintenance(vehicleID):
    """
    Route for report vehicle page of the website

    Parameters:
       vehicleID(Integer): Vehicle ID from the database 

    Returns:
        return redirect(url_for('dashboard')): Redirect to Admin dashboard
        return render_template('report_vehicle.html', form=form): Render the report vehicle HTML page 
    """
    obj = requestsUtil()
    form = MaintenanceForm(request.form)
    engineerResult = obj.get_engineers()
    result = obj.get_vehicle(vehicleID)

    dropdownValue = []

    for i in engineerResult:
        dropdownValue.append(i['engineerUsername'])

    tupleDropDownValue = [(val, val) for val in dropdownValue]

    form.engineerName.choices = tupleDropDownValue

    if request.method == 'POST' and form.validate():
        apiKey = "o.spfQSePwyGKGMeZG8DZxXZRJIMmSli0X"
        p = PushBullet(apiKey)

        vehicleID = result['vehicleID']
        vehicleModel = result['vehicleModel']
        longitude = result['longitude']
        latitude = result['latitude']
        engineerName = request.form['engineerName']
        engineerDevice = ""
        engineerDeviceID = ""

        for i in engineerResult:
            if i['engineerUsername'] == engineerName:
                engineerDevice = i['engineerDevice']
                engineerDeviceID = i['engineerDeviceID']

        obj.add_maintenance(vehicleID, vehicleModel, longitude,
                            latitude, engineerName, engineerDevice, engineerDeviceID)
        dev = p.get_device(engineerDevice)
        push = dev.push_note(
            "NOTICE: ", "A new vehicle has been assigned to you for maintenence!!")
        flash('Vehicle Reported', 'success')

        return redirect(url_for('dashboard'))

    return render_template('report_vehicle.html', form=form)


class Vehicle:
    obj = requestsUtil()
    results = obj.get_maintenance()

    longitude = []
    latitude = []
    vehicleModel = []

    for i in results:
        longitude.append(i['longitude'])
        latitude.append(i['latitude'])
        vehicleModel.append(i['vehicleModel'])

    zipped = zip(latitude, longitude, vehicleModel)

    result_set = set(zipped)

    latlng = [list(item) for item in result_set]


@app.route("/vehicle_locations")
@is_logged_in
def vehicle_locations():
    """
    Route for vehicle location page of the website

    Parameters:
       None

    Returns:
        return redirect(url_for('dashboard')): Redirect to Admin dashboard
        return render_template('report_vehicle.html', form=form): Render the report vehicle HTML page 
    """
    username = session['username']

    obj = requestsUtil()
    results = obj.get_maintenance()

    longitude = []
    latitude = []
    vehicleModel = []

    for i in results:
        if i['engineerName'] == username:
            longitude.append(i['longitude'])
            latitude.append(i['latitude'])
            vehicleModel.append(i['vehicleModel'])

    zipped = zip(latitude, longitude, vehicleModel)

    result_set = set(zipped)

    latlng = [list(item) for item in result_set]

    if latlng:
        return render_template('map.html', latlng=latlng)
    else:
        abort(404)


@app.route("/manager_dashboard")
@is_logged_in
def manager_dashboard():
    """
    Route for manager dashboard page of the website

    Parameters:
       None

    Returns:
         return render_template('manager_dashboard.html'): Render the dashboard for manager
    """
    obj = requestsUtil()
    data = obj.get_records()

    hondaCounter = 0
    toyotaCounter = 0
    nissanCounter = 0
    fordCounter = 0
    mazdaCounter = 0

    onedayCounter = 0
    twodayCounter = 0
    fourdayCounter = 0

    percentOne = 0
    percentTwo = 0
    percentFour = 0
    total = 0

    for i in data:
        if i['vehicle']['vehicleBrand'] == 'Honda':
            hondaCounter = hondaCounter + 1
        elif i['vehicle']['vehicleBrand'] == 'Toyota':
            toyotaCounter = toyotaCounter + 1

    for i in data:
        if i['daysRented'] == 1:
            onedayCounter = onedayCounter + 1
        elif i['daysRented'] > 1 and i['daysRented'] < 4:
            twodayCounter = twodayCounter + 1
        elif i['daysRented'] > 4:
            fourdayCounter = fourdayCounter + 1

    total = onedayCounter + twodayCounter + fourdayCounter

    percentOne = onedayCounter/total*1

    percentTwo = twodayCounter/total*1
    if fourdayCounter == 0:
        percentFour = 0
    else:
        percentFour = fourdayCounter/total*1

    titleBar = 'Brands of vehicle that customers prefer to rent(Number of Times)'
    titleLine = 'Number of rentals for year 2019(Number of Rentals)'
    titlePie = 'How many days customers usually rent a vehicle(Percentage %)'
    bar_labels = [
        'Toyota', 'Nissan', 'Honda', 'Ford',
        'Mazda'
    ]

    bar_values = [
        toyotaCounter, nissanCounter, hondaCounter, fordCounter,
        mazdaCounter
    ]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    labels_line = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    values_line = [
        30, 25, 20, 15,
        35, 40, 44, 43,
        20, 33, 42, 33
    ]

    values = [
        percentOne, percentTwo, percentFour
    ]

    labels = [
        '1 Day', '2 to 3 Days', 'More than 3 Days'
    ]
    bar_labels = bar_labels
    bar_values = bar_values
    return render_template('manager_dashboard.html', titleBar=titleBar, titleLine=titleLine, titlePie=titlePie, max=max(toyotaCounter, nissanCounter, fordCounter, mazdaCounter, hondaCounter), maxLine=50, pieMax=100, bar_labels=bar_labels, labels_line=labels_line, values_line=values_line, bar_values=bar_values, set=zip(values, labels, colors))


@app.route('/rental_records', methods=['GET', 'POST'])
@is_logged_in
def rental_records():
    """
    Route for rental records page of the website

    Parameters:
        None

    Returns:
        return render_template('rental_records.html', recordsData=recordsData): Render the rental records page for the site
    """
    obj = requestsUtil()
    recordsData = obj.get_records()

    return render_template('rental_records.html', recordsData=recordsData)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
