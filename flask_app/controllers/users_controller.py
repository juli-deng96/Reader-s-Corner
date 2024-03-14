from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import User


# ===============Login Form Submission Route

@app.route('/')
def first_page():
    return render_template('index.html') 

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_users_username(request.form)
    session['uid'] = user.id
    if 'uid' in session:
        return redirect ('/homepage')
    return redirect('/homepage')

# ======================== Register Route

# Register Page Route
@app.route('/registration', methods=['GET'])
def register_page():
    return render_template('register.html')

# Register Form Submission Route
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/registration')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashed_password
    }
    session['uid'] = User.create(user_data)
    return redirect('/')

# ============================Logout Route

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')