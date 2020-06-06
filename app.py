from flask import Flask, render_template, request, session, url_for, flash, redirect
from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.validators import InputRequired
from requestsUtil import requestsUtil
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
            if results.get("adminPassword") == password_candidate:
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Password incorrect"
                app.logger.info('PASSWORD NOT MATCHED')
        else:
            error = "Username not found"
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
        obj.add_user(username, firstname, surname, password, imageName)

        flash('User Added', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_user.html', form=form)

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
    cost = [15,20,25]
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

    return render_template('add_vehicle.html', form=form, cost=cost)

class SearchUser(Form):
    category = SelectField('Catergory', choices=[("username", "Username"), ("firstname", "First Name"), ("surname", "Surname")])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])

@app.route('/search_user', methods=['GET', 'POST'])
@is_logged_in
def searchUser():
    data = {}
    form = SearchUser(request.form)
    objRec = requestsUtil()
    if request.method == "POST" and form.validate():
        keyword = form.keyword.data
        category = form.category.data
        results = objRec.get_users()
        data = objRec.search(keyword, category, results)

        return render_template('searchUser.html', data=data, form=form)
    else:     
        return render_template('searchUser.html',form=form, data=data)

if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)