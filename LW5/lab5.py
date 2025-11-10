import os # Работа с переменными окружения (cекретными ключами и строками подключения)
from dotenv import load_dotenv #чтобы читать переменные из .env
from flask import (
    Flask, render_template, redirect, url_for, request, flash
)

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
#UserMixin - базовый класс, который добавляет методы для работы с пользователями
from werkzeug.security import generate_password_hash, check_password_hash # Для хеширования паролей
from sqlalchemy.exc import SQLAlchemyError # Для обработки ошибок базы данных

# --- Загружаем переменные окружения ---
load_dotenv()

# --- Настройка Flask ---
app = Flask(__name__) # Создаём экземпляр Flask-приложения, '__name__' указывает на текущий модуль

# Используем значения из .env (если не найдены — подставляются дефолтные)
app.secret_key = os.environ.get("FLASK_SECRET", "super_secret_key_123")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", # Читаем строку подключения к базе данных из .env
    "postgresql://postgres:1111@localhost/LW_5" # Если нет в .env, используем дефолтную строку подключения
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Отключаем отслеживание изменений объектов для повышения производительности

# --- Инициализация БД и Flask-Login ---
db = SQLAlchemy(app)  # Инициализируем объект для работы с базой данных через SQLAlchemy
login_manager = LoginManager(app)  # Инициализируем менеджер для работы с сессиями пользователей
login_manager.login_view = 'login'  # Указываем, на какой маршрут перенаправлять неавторизованных пользователей


# --- Модель пользователя ---
class User(UserMixin, db.Model):  # Наследуем модель от UserMixin (для использования с Flask-Login) и db.Model (для работы с БД)
    __tablename__ = 'users'  # Указываем название таблицы в базе данных

    id = db.Column(db.Integer, primary_key=True) # Уникальный идентификатор пользователя
    name = db.Column(db.String(100), nullable=False) # Имя пользователя, не может быть пустым
    email = db.Column(db.String(100), unique=True, nullable=False) # Email, который уникален
    password = db.Column(db.String(200), nullable=False) # Пароль (будет храниться в хешированном виде)


@login_manager.user_loader
def load_user(user_id):  # Функция для загрузки пользователя по ID
    return User.query.get(int(user_id))  # Возвращаем пользователя из базы по ID

@app.route('/')
def index():  # Главная страница
    if current_user.is_authenticated:  # Проверяем, авторизован ли пользователь
        return render_template('index.html', name=current_user.name)  # Если да, рендерим главную страницу с именем пользователя
    return redirect(url_for('login'))  # Если нет — перенаправляем на страницу входа


@app.route('/login', methods=['GET', 'POST'])
def login():  # Страница логина
    if request.method == 'POST':  # Если запрос POST (пользователь отправил форму)
        email = request.form.get('email', '').strip()  # Получаем email из формы и убираем пробелы
        password = request.form.get('password', '').strip()  # Получаем пароль и убираем пробелы

        if not email or not password: # Если поля пустые, показываем ошибку
            flash('Заполните все поля!')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first() # Ищем пользователя по email в базе, если не найден — показываем ошибку
        if not user:
            flash('Пользователь не найден!')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password): # Проверяем хеш пароля, если не совпадает — показываем ошибку
            flash('Неверный пароль!')
            return redirect(url_for('login'))

        login_user(user) # Авторизуем пользователя
        flash('Вы успешно вошли!')
        return redirect(url_for('index')) # Перенаправляем на главную страницу после успешного входа

    return render_template('login.html') # Если метод GET, отображаем страницу логина

#Страница регистрации
@app.route('/signup', methods=['GET', 'POST'])
def signup():  # Страница регистрации
    if request.method == 'POST':  # Если запрос POST (пользователь отправил форму)
        name = request.form.get('name', '').strip()  # Получаем имя из формы и убираем пробелы
        email = request.form.get('email', '').strip()  # Получаем email
        password = request.form.get('password', '').strip()  # Получаем пароль

        if not (name and email and password):  # Проверяем, что все обязательные поля заполнены
            flash('Все поля обязательны!')  # Показываем сообщение об ошибке
            return redirect(url_for('signup'))  # Перенаправляем назад на страницу регистрации

        if len(password) < 6:  # Проверяем, что пароль не короче 6 символов
            flash('Пароль должен содержать не менее 6 символов!')  # Показываем сообщение об ошибке
            return redirect(url_for('signup'))  # Перенаправляем назад на страницу регистрации

        if User.query.filter_by(email=email).first():  # Проверяем, есть ли уже пользователь с таким email
            flash('Пользователь с таким email уже существует!')  # Показываем сообщение об ошибке
            return redirect(url_for('signup'))  # Перенаправляем назад на страницу регистрации

        try:
            hashed_password = generate_password_hash(password)  # Хешируем пароль
            new_user = User(name=name, email=email, password=hashed_password)  # Создаём нового пользователя
            db.session.add(new_user)  # Добавляем пользователя в сессию базы данных
            db.session.commit()  # Сохраняем изменения в базе данных
        except SQLAlchemyError:  # Если возникает ошибка при работе с базой данных
            db.session.rollback()  # Откатываем изменения
            flash('Ошибка при сохранении данных. Попробуйте снова.')  # Показываем сообщение об ошибке
            return redirect(url_for('signup'))  # Перенаправляем назад на страницу регистрации

        flash('Регистрация успешна! Теперь войдите в систему.')  # Показываем сообщение об успешной регистрации
        return redirect(url_for('login'))  # Перенаправляем на страницу входа

    return render_template('signup.html')  # Если метод GET, отображаем страницу регистрации

#Страница выхода
@app.route('/logout')
@login_required  # Защищаем маршрут от неавторизованных пользователей
def logout():  # Функция для выхода пользователя
    logout_user()  # Завершаем сессию пользователя
    flash('Вы вышли из аккаунта.')  # Показываем сообщение о выходе
    return redirect(url_for('login'))  # Перенаправляем на страницу входа

#Создание таблиц в базе данных и запуск приложения
if __name__ == '__main__':
    with app.app_context():  # Создаём контекст приложения для работы с базой данных
        db.create_all()  # Создаём все таблицы в базе данных (если их ещё нет)
    app.run(debug=True)  # Запускаем Flask-приложение в режиме отладки