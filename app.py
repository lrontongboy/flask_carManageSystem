from flask import Flask, render_template, url_for, request, session, redirect, jsonify, g
from models.user import User
from models.car import Car
from pagination import Pagination
from password_encryptor import encrypt_password, check_password_hash
from models.reservation import Reservation
from decorations import admin_login, user_login
import os
from datetime import date, datetime, timedelta
app = Flask(__name__)
app.secret_key = os.urandom(24) 

@app.before_request
def check_for_login():
    if request.endpoint in ['login', 'login_form', 'registrate', 'registration_form'] or request.path.startswith('/static/'):
        pass
    elif 'logged_in' in session and session['logged_in'] and 'user_id' in session:  # 检查 'id' 是否存在
        app.user = User.find(session['user_id'])
        g.user = app.user.to_dict()
    else:
        print(session)
        return redirect('/login_form')
    

@app.route('/registration_form')
def registration_form():
    return render_template('registration_form.html')

@app.route('/registrate', methods=['POST'])
def registrate():
    username = request.form['username']
    if User.findByUsername(username):
        return jsonify({'success': False, 'error_message': 'The username has been taken!'})
    elif request.form['password'] != request.form['confirm_password']:
        return jsonify({'success': False, 'error_message': 'The passwords entered twice do not match!'})
    else:
        encrypted_password = encrypt_password(request.form['password'])
        new_user = User(username=username, password=encrypted_password)
        new_user.save()
        login_helper(new_user)
        return jsonify({'success': True})

@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    user = User.findByUsername(username)
    if not user: 
        return jsonify({'success': False, 'error_message': 'User not found!'})
    encrypted_password = encrypt_password(request.form['password'])
    if user.authenticate(request.form['password']):
    # if user.authenticate(encrypted_password):
        login_helper(user)
        return jsonify({'success': True, 'redirect': '/'}) 
    else: 
        return jsonify({'success': False, 'error_message': 'Incorrect password!'})
    
def login_helper(user):
    session['logged_in'] = True
    session['user_id'] = user.getID()
    session['is_admin'] = user.isAdmin()
    app.user = user

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    app.user = None
    return redirect('/login_form')


@app.route('/profile', methods=['GET', 'POST'])
@user_login
def profile():
    if request.method == 'POST':
        g.user.update_profile(
            request.form['real_name'],
            request.form['date_of_birth'],
            request.form['address']
        )
        return redirect('/')  #  Redirect to the homepage or another page
    else:
        user = User.find(session['user_id'])
        reservations = Reservation.findByUserID(user.getID())
        return render_template('profile.html', user=user, reservations=reservations)

@app.route('/reservation', methods=['GET', 'POST'])
@user_login
def reservation():
    if request.method == 'POST':
        car_id = int(request.form['car_id'])
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']

        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

        # check timestamp
        if Reservation.check_conflict(car_id, start_time, end_time):
            return jsonify({'status': 'error', 'message': 'The selected time slot has already been booked, please choose another time.'}), 400

        new_reservation = Reservation(None, session['user_id'], car_id, start_time, end_time)
        new_reservation.save()
        return jsonify({'status': 'success', 'message': url_for('index')}), 200
    else:
        car_id = request.args.get('car_id')
        return render_template('reservation.html', car_id=car_id)

@app.route('/')
def index():
    cars = Car.allAvailable()
    users = User.all()
    return render_template('index.html', cars=cars, user=users)

@app.route('/car/<int:car_id>')
def car_info(car_id):
    car = Car.find(car_id)
    return render_template('car_info.html', car=car)

@app.route('/reserve/<int:car_id>')
@user_login
def reserve_info(car_id):
    car = Car.find(car_id)
    return render_template('reserve_info.html', car=car)

@app.route('/admin')
@admin_login
def admin():
    return render_template('admin.html')

@app.route('/admin/cars')
@admin_login
def admin_cars():
    cars = Car.all()
    return render_template('admin_cars.html', cars=cars)

@app.route('/admin/reservations')
@admin_login
def admin_reserve():
    reservations = Reservation.all()
    return render_template('admin_reserve.html', reservations=reservations)


@app.route('/admin/register_user', methods=['GET'])
@admin_login
def users():
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = (page - 1) * per_page

    # Get all users
    users = User.all()
    total_users = len(users)

    # Paging processing
    paginated_users = users[offset:offset + per_page]
    total_pages = (total_users + per_page - 1) // per_page
    pagination = Pagination(page, per_page, total_users, paginated_users)

    return render_template('admin/register_user.html', title='user manage', pagination=pagination)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@admin_login
def add_user():
    if request.method == 'GET':
        return render_template('admin/add_user.html', title='add user')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        real_name = request.form.get('real_name')
        date_of_birth_str = request.form.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date() if date_of_birth_str else None
        address = request.form.get('address')
        is_admin = request.form.get('is_admin') == '1'  

        
        existing_user = User.findByUsername(username)
        if existing_user:
            return jsonify({'status': 'error', 'message': '用户名已存在'}), 200

        
        new_user = User(username=username, password=password, real_name=real_name, 
                        date_of_birth=date_of_birth, address=address, is_admin=is_admin)
        new_user.save()

        return jsonify({'status': 'success', 'message': '添加成功'}), 200

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=5500)
