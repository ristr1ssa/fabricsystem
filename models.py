from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt

# data = [20.0, 10.0, 5.0, 1.0, 0.5]

#     # Метки для секторов графика
#     labels = ["data1", "data2", "data3", "data4", "data5"]

#     # И снова нарисуем график
#     plt.pie (data, labels=labels)

#     plt.show()


# Инициализация Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9009@185.13.113.182:5432/fabric'
db = SQLAlchemy(app)


# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Перенаправляет на login, если пользователь не авторизован
login_manager.login_view = 'login'


# Модель пользователя
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(7))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Orders(db.Model):
    article = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, default=0)


class ActiveOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def is_admin(username) -> bool:
    user = db.session.query(Users).filter_by(
        role='admin', username=username).one_or_none()
    return user is not None


def get_users_fromDB():
    users = db.session.query(
        Users.id, Users.username, Users.role).filter(Users.role != 'admin').all()

    result = [{"id": user.id, "username": user.username, "role": user.role}
              for user in users]
    return result


def get_orders_from_db():
    orders = db.session.query(
        Orders.article, Orders.name, Orders.price).all()

    result = [{"article": order.article, "name": order.name, "price": order.price}
              for order in orders]
    return result


def get_active_orders_from_db():
    pass


def del_user_from_db(uid):
    uid = int(uid)
    try:
        user = Users.query.filter(Users.id == uid).first()
        db.session.delete(user)
        db.session.commit()
        return Response(status=200)
    except Exception:
        return Response(status=404)


def add_order_to_db(article, name, price):
    try:
        order = Orders(article=article, name=name, price=price)
        db.session.add(order)
        db.session.commit()
        return Response(status=200)
    except Exception:
        return Response(status=404)


def avtive_order_db(action, article):
    if action == 'DEL':
        pass
    elif action == "ADD":
        data = Orders.query.filter(Orders.article == article).first()
        print(data)
        # data = ActiveOrders(data.art)


with app.app_context():
    db.create_all()
