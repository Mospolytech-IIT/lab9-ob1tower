"""
Лабораторная работа №9: Работа с базой данных через SQLAlchemy.
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

# Строка подключения для SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создание движка для работы с SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    """
    pass

class User(Base):
    """
    Модель Users.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # Целое число, первичный ключ, автоинкремент
    username = Column(String, unique=True, index=True)  # Строка, уникальное значение
    email = Column(String, unique=True, index=True)  # Строка, уникальное значение
    password = Column(String)  # Строка

class Post(Base):
    """
    Модель Posts.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)  # Целое число, первичный ключ, автоинкремент
    title = Column(String)  # Строка
    content = Column(Text)  # Текст
    # Целое число, внешний ключ, ссылающийся на поле id таблицы Users
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="posts", passive_deletes=True)
