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

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Введите ниже данные пользователя")
    # запрашиваем у пользователя данные
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    
    gender_validated = False
    while gender_validated == False:
        gender = input("Пол (Male / Female): ")
        if validate_gender(gender):
            gender_validated = True

    email_validated = False
    while email_validated == False:
        email = input("Адрес электронной почты: ")
        if validate_email(email):
            email_validated = True

    birthdate_validated = False
    while birthdate_validated == False:
        birthdate = input("Дата рождения (в формате 1900-01-01): ")
        if validate_birthdate(birthdate):
            birthdate_validated = True

    height_validated = False
    while height_validated == False:
        height = input("Рост: (в формате 1.99): ")
        if validate_height(height):
            height_validated = True

    # создаем нового пользователя
    user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )
    # возвращаем созданного пользователя
    return user

def validate_gender(gender):
    if gender == "Male" or gender == "Female":
        return True
    else:
        print("Неправильное значение пола")
        return False

def validate_email(email):
    """
    Валидация адреса электронной почты
    """
    if "@" in email:
        if email.count("@") > 1:
            print("В адресе более одного символа @")
            return False
        else:
            domain = email.split("@")[1]
            if "." in domain:
                if domain.count(".") > 1:
                    print("В домене более одного символа .")
                    return False
                if len(domain.split(".")[0]) < 2 or len(domain.split(".")[1]) < 2:
                    print("В домене до и после точки должно быть хотя бы 2 символа")
                    return False
                return True
            else:
                print("В домене отсутствует .")
                return False
    else:
        print("В адресе отсутствует @")
        return False

def validate_birthdate(birthdate):
    """
    Валидация даты рождения
    """
    if birthdate.count("-") != 2:
        print("Дата рождения должна содержать 2 дефиса")
        return False
    else:
        year = birthdate.split("-")[0]
        if len(year) != 4:
            print("Год должен состоять из 4 символов")
            return False
        if int(year) < 1900 or int(year) > 2020:
            print("Год рождения может быть задан в промежутке от 1900 до 2020 годов")
            return False
        month = birthdate.split("-")[1]
        if len(month) != 2:
            print("Месяц должен состоять из 2 символов")
            return False
        if int(month) < 1 or int(month) > 12:
            print("Месяц рождения может быть задан в промежутке от 01 до 12")
            return False
        day = birthdate.split("-")[2]
        if len(day) != 2:
            print("День должен состоять из 2 символов")
            return False
        if int(day) < 1 or int(day) > 31:
            print("День рождения может быть задан в промежутке от 01 до 31")
            return False
        return True

def validate_height(height):
    """
    Валидация роста
    """
    if height.count(".") != 1:
        print("Значение роста должно содержать точку")
        return False
    else:
        if len(height.split(".")[0]) < 1 and len(height.split(".")[1]) < 1:
            print("До или после точки должен быть хотя бы один символ")
            return False
        if float(height) < 1 or float(height) > 3:
            print("Рост может быть задан в диапазоне 1.00..3.00")
            return False
        return True

def print_all_users(session):
    """
    Печать всех имеющихся пользователей из таблицы user
    """
    query = session.query(User).all()

    for user in query:
        print(f"{user.id} | {user.first_name} | {user.last_name} | {user.gender} | {user.email} | {user.birthdate} | {user.height}")

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выберите режим.\n1 - создание нового пользователя\n2 - вывод всех пользователей\n")
    # проверяем режим
    if mode == "1":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    elif mode == "2":
        # печатаем всех пользователей
        print_all_users(session)
    else:
        print("Некорректный режим:(")

if __name__ == "__main__":
    main()