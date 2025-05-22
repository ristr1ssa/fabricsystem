from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from models import app, db, Users, is_admin, get_users_fromDB, del_user_from_db, get_orders_from_db, get_active_orders_from_db, add_order_to_db, avtive_order_db


# 📌 Главная страница (только для авторизованных)
@app.route('/')
@login_required
def home():
    return render_template('test_manager_main.html')


# 📌 Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if is_admin(username):
                return render_template('test_admin_panel.html')
            login_user(user)
            return render_template('test_manager_main.html')
    return render_template('login.html')


# 📌 Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        role = request.form.get('role')
        if Users.query.filter_by(username=username).first():
            return 'Пользователь уже существует!'

        new_user = Users(username=username)
        new_user.set_password(password)  # хешируем пароль
        new_user.role = role  # задаем роль
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    elif request.method == 'GET':
        username = request.args.get('user')
        password = request.args.get('pass')
        role = request.args.get('role')

        if Users.query.filter_by(username=username).first():
            return 'Пользователь уже существует!'

        new_user = Users(username=username)
        new_user.set_password(password)  # хешируем пароль
        new_user.role = role  # задаем роль
        db.session.add(new_user)
        db.session.commit()
        return "Done"
    return "error"


@app.route('/del-user', methods=['GET'])
def del_user():
    uid = request.args.get('uid')
    return del_user_from_db(uid)


@app.route('/get-active-users')
def get_active_users_data():
    users = get_users_fromDB()
    return users


@app.route('/get-orders')
def get_orders():
    orders = get_orders_from_db()
    return orders


@app.route('/get-active-orders')
def get_active_orders():
    orders = get_active_orders_from_db()
    return orders


@app.route('/add-order')
def add_order():
    name = request.args.get('name')
    article = request.args.get('article')
    price = request.args.get('price')
    return add_order_to_db(name=name, article=article, price=price)


@app.route('/active-orders')
def del_order_active():
    action = request.args.get('action')
    article = request.args.get('article')
    return avtive_order_db(action, article)

# 📌 Выход из системы


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
