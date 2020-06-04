from flask import Flask, render_template, redirect, url_for, flash, request, g, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, SelectField
from wtforms.validators import InputRequired, Email, Length
import os
from requestsUtil import requestsUtil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissuppose'
Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.Regexp('^\w+$', message="Username must contain only letters numbers or underscore"),
        validators.Length(min=5, max=25, message="Username must be betwen 5 & 25 characters")
    ])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=12)])
    remember = BooleanField('remember me')

class Search(FlaskForm):
    field = SelectField('Catergory', choices=[('colour', 'Colour'), ('vehicleBrand', 'Brand'), ('vehicleModel', 'Model')])
    keyword = StringField('Enter Keyword:', validators=[InputRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session.pop('user', None)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            obj = requestsUtil(str(username))
            #objRec = requestsUtil()
            
            #testData = objRec.get_records()
            
            data = obj.get_admin()
            status = not bool(data) 

            if status == True:
                flash("Incorrect Username or Username does not exist!!!")
                return redirect(url_for('login'))
            elif data.get("adminUsername") == username and data.get("adminPassword") == form.password.data:
                session['user'] = form.username.data
                #return '<h1>' + str(testData) + '<h1>'
                return redirect(url_for('adminDashboard'))
            else:
                flash("Incorrect Password!!!")

    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/adminDashboard')
def adminDashboard():
    if g.user:
        return render_template('adminDashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/records')
def records():
    if g.user:
        objRec = requestsUtil()    
        recordsData = objRec.get_records()
        return render_template('records.html', recordsData=recordsData)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = {}
    form = Search()
    objRec = requestsUtil()
    if request.method == "POST":
        if form.validate_on_submit():
            keyword = form.keyword.data
            category = form.field.data
            apiData = objRec.get_vehicles()
            data = objRec.search(keyword, category, apiData)
            return render_template('search.html', data=data, form=form)
    else:     
        return render_template('search.html',form=form, data=data)
    

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

if __name__ == '__main__':
    app.run(debug=True)