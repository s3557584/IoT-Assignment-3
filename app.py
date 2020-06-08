from flask import Flask, render_template, request, session, url_for, flash, redirect
from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.validators import InputRequired
from requestsUtil import requestsUtil
from pushbullet.pushbullet import PushBullet

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    obj = requestsUtil()
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        results = obj.get_admin(username)
        status = not bool(results) 
        
        if status != True:

            decryptedPassword = obj.decryptPassword(results.get("adminPassword"))

            if decryptedPassword == password_candidate:
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Password incorrect!!!"
                return render_template('login.html', error=error)
        else:
            return render_template('login.html', error=error)
    
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
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
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

class UserForm(Form):
    username = StringField('Username', [validators.length(min=1, max=50)])
    firstname =  StringField('First Name', [validators.length(min=1, max=50)])
    surname =  StringField('Surname', [validators.length(min=1, max=50)])
    password =  StringField('Password', [validators.length(min=1, max=50)])
    imageName =  StringField('Image Name', [validators.length(min=1, max=50)])

@app.route('/add_user', methods=['GET', 'POST'])
@is_logged_in
def add_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        firstname = form.firstname.data
        surname = form.surname.data
        password = form.password.data
        imageName = form.imageName.data

        obj = requestsUtil()

        encryptedPassword = obj.encryptPassword(password)

        obj.add_user(username, firstname, surname, encryptedPassword, imageName)

        flash('User Added', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_user.html', form=form)

@app.route('/edit_user/<string:userID>', methods=['GET', 'POST'])
@is_logged_in
def edit_user(userID):
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
        obj.update_user(userID, username, firstname, surname, encryptedPassword, imageName)

        flash('User Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_user.html', form=form)

class VehicleForm(Form):
    brand = StringField('Brand', [validators.length(min=1, max=50)])
    colour =  StringField('Colour', [validators.length(min=1, max=50)])
    cost = SelectField('Cost', choices=[("15","15"), ("20","20"), ("25","25")])
    seats = SelectField('Seats', choices=[("2","2"), ("4","4"), ("7","7")])
    model =  StringField('Model', [validators.length(min=1, max=50)])

@app.route('/add_vehicle', methods=['GET', 'POST'])
@is_logged_in
def add_vehicle():
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
        obj.update_vehicle(vehicleID, vehicleBrand, colour, cost, seats, vehicleModel)

        flash('Vehicle Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_vehicle.html', form=form)

class SearchUser(Form):
    category = SelectField('Catergory', choices=[("username", "Username"), ("firstname", "First Name"), ("surname", "Surname")])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])

@app.route('/search_user', methods=['GET', 'POST'])
@is_logged_in
def searchUser():
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
    
    return render_template('searchUser.html',form=form)

class SearchVehicle(Form):
    category = SelectField('Catergory', choices=[('colour', 'Colour'), ('vehicleBrand', 'Brand'), ('vehicleModel', 'Model')])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])

@app.route('/search_vehicle', methods=['GET', 'POST'])
@is_logged_in
def searchVehicle():
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
    
    return render_template('searchVehicle.html',form=form)

@app.route('/delete_vehicle/<string:vehicleID>', methods=['GET', 'POST'])
@is_logged_in
def deleteVehicle(vehicleID):

    obj = requestsUtil()
    obj.delete_vehicle(vehicleID)

    flash('Vehicle Deleted', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_user/<string:userID>', methods=['GET', 'POST'])
@is_logged_in
def deleteUser(userID):

    obj = requestsUtil()
    obj.delete_user(userID)

    flash('User Deleted', 'success')
    
    return redirect(url_for('dashboard'))

class MaintenanceForm(Form):
    engineerName = SelectField('Engineer')

@app.route('/report_vehicle/<string:vehicleID>', methods=['GET', 'POST'])
@is_logged_in
def add_maintenance(vehicleID):
    obj = requestsUtil()
    form = MaintenanceForm(request.form)
    engineerResult = obj.get_engineers()
    result = obj.get_vehicle(vehicleID)
    
    dropdownValue = []
    
    for i in engineerResult:
        dropdownValue.append(i['engineerUsername'])
    
    tupleDropDownValue = [(val,val) for val in dropdownValue]
    
    form.engineerName.choices = tupleDropDownValue

    if request.method == 'POST' and form.validate():
        apiKey = "o.spfQSePwyGKGMeZG8DZxXZRJIMmSli0X"
        p = PushBullet(apiKey)



        vehicleID = result['vehicleID']
        vehicleModel = result['vehicleModel']
        longitude = result['longitude']
        latitude = result['latitude']
        engineerName = request.form['engineerName']
        engineerEmail = ""
        
        for i in engineerResult:
            if i['engineerUsername'] == engineerName:
                engineerEmail = i['engineerEmail']

        obj.add_maintenance(vehicleID, vehicleModel, longitude, latitude, engineerName, engineerEmail)
        p.pushNote(engineerEmail, 'Vehicle Required Maintenence', 'A vehicle has been assigned to you for maintenence', recipient_type='email')

        flash('Vehicle Reported', 'success')

        return redirect(url_for('dashboard'))

    return render_template('report_vehicle.html', form=form)

if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)