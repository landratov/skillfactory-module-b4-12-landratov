import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key = True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)

class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения данных об атлетах
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key = True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост атлета
    height = sa.Column(sa.Float)
    # имя атлета
    name = sa.Column(sa.Text)
    # вес атлета
    weight = sa.Column(sa.Integer)
    # кол-во золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # кол-во серебряных медалей
    silver_medals = sa.Column(sa.Integer)
    # кол-во бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # общее кол-во медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def convert_str_to_date(date_str):
    """
    Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def find_user(user_id, session):
    query = session.query(User).filter(User.id == user_id)

    if query.count() < 1:
        print(f"Пользователь с id = {user_id} не найден")
    else:
        return query.first()

def find_nearest_athletes_by_birthdate(user, session):
    query = session.query(Athelete).all()

    min_value = None
    bd_athlete = None

    for athelete in query:
        diff = abs(convert_str_to_date(athelete.birthdate) - convert_str_to_date(user.birthdate))
        if not min_value or diff <= min_value:
            min_value = diff
            bd_athlete = athelete

    print(f"Дата рождения пользователя: {user.birthdate}")
    print(f"Ближайший по дате рождения атлет: {bd_athlete.id} {bd_athlete.name} {bd_athlete.birthdate}")

def find_nearest_athletes_by_height(user, session):
    query = session.query(Athelete).filter(Athelete.height != None)

    min_value = None
    height_athlete = None

    for athelete in query:
        diff = abs(athelete.height - user.height)
        if not min_value or diff <= min_value:
            min_value = diff
            height_athlete = athelete

    print(f"Рост пользователя: {user.height}")
    print(f"Ближайший по росту атлет: {height_athlete.id} {height_athlete.name} {height_athlete.height}")

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()

    user_id = input("Введите id пользователя для поиска похожего атлета: ")
    user = find_user(user_id, session)
    find_nearest_athletes_by_birthdate(user, session)
    find_nearest_athletes_by_height(user, session)

if __name__ == "__main__":
    main()