import os
from dotenv import load_dotenv
from flask import (
    Flask, render_template, redirect, url_for, request, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

# --- Загружаем переменные окружения ---
load_dotenv()

# --- Настройка Flask ---
app = Flask(__name__)

# Используем значения из .env (если не найдены — подставляются дефолтные)
app.secret_key = os.environ.get("FLASK_SECRET", "super_secret_key_123")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:1111@localhost/LW_5"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Инициализация БД и Flask-Login ---
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# --- Модель пользователя ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.name)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Заполните все поля!')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Пользователь не найден!')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Неверный пароль!')
            return redirect(url_for('login'))

        login_user(user)
        flash('Вы успешно вошли!')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not (name and email and password):
            flash('Все поля обязательны!')
            return redirect(url_for('signup'))

        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов!')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует!')
            return redirect(url_for('signup'))

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Ошибка при сохранении данных. Попробуйте снова.')
            return redirect(url_for('signup'))

        flash('Регистрация успешна! Теперь войдите в систему.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)