from flask import render_template, flash, redirect, url_for, request, json
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db
from app.forms import RegistrationForm
import requests;



app.debug = True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
	data = json.loads(requests.get('https://jsonplaceholder.typicode.com/todos').content) #получаем список
	todos = []
	flag = current_user.id % 2 #флаг четный или нечетный id
	for i in data:
		if (i['id'] % 2) == 0: #проверяем чет или не чет
			if(flag):
				continue
			else:
				todos.append(i)
		else:
			if(flag):
				todos.append(i)
			else:
				continue
					
	return render_template('index.html', todos = todos)