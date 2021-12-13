from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/index')

@app.route('/index')
def users():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['id'] = User.create(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.getByEmail(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    session['id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data ={
        'id': session['id']
    }
    return render_template("dashboard.html", user = User.getById(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')