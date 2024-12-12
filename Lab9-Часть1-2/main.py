"""
Лабораторная работа №9: Работа с базой данных через SQLAlchemy.
"""
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Строка подключения для SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создание движка для работы с SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


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

    # Целое число, первичный ключ, автоинкремент
    id = Column(Integer, primary_key=True, index=True)
    # Строка, уникальное значение
    username = Column(String, unique=True, index=True)
    # Строка, уникальное значение
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Строка


class Post(Base):
    """
    Модель Posts.
    """
    __tablename__ = "posts"

    # Целое число, первичный ключ, автоинкремент
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)  # Строка
    content = Column(Text)  # Текст
    # Целое число, внешний ключ, ссылающийся на поле id таблицы Users
    user_id = Column(Integer, ForeignKey("users.id"))


# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание сессии базы данных
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

# Создание экземпляра FastAPI
app = FastAPI()

# Добавляется пользователей
user1 = User(username="Елизавета", email="eliz@bk.ru", password="eliz123")
user2 = User(username="Арина", email="arisha@bk.ru", password="arisha123")
user3 = User(username="Даша", email="dasha@bk.ru", password="dasha123")

db.add_all([user1, user2, user3])  # Добавляется всех пользователей сразу
db.commit()  # Сохраняется изменения

# Добавляется посты
post1 = Post(title="Первый",
             content="Всем привет!", user_id=1)
post2 = Post(title="Второй",
             content="Что делаешь?", user_id=2)
post3 = Post(title="Третий",
             content="Как день прошел?", user_id=1)

db.add_all([post1, post2, post3])  # Добавляется посты
db.commit()  # Сохраняется изменения

# Извлекается всех пользователей
users = db.query(User).all()
print("Все пользователи:")
for user in users:
    print(f"{user.id}: {user.username} ({user.email})")

# Извлекается все посты с информацией о пользователях
posts = db.query(Post).all()
print("\nВсе посты:")
for post in posts:
    user = db.query(User).filter(User.id == post.user_id).first()
    print(f"{post.id}: {post.title} - Автор: {user.username}")

# Извлекается посты, созданные конкретным пользователем
user_posts = db.query(Post).filter(Post.user_id == 1).all()
print("\nПосты пользователя с id=1:")
for post in user_posts:
    print(f"{post.id}: {post.title}")

# Обновляется email у 1 пользователя
user_to_update = db.query(User).filter(User.id == 1).first()
if user_to_update:
    user_to_update.email = "new_email@bk.ru"
    db.commit()
    print(f"\nEmail пользователя {user_to_update.username} обновлен.")

# Обновляется содержимое 1 поста
post_to_update = db.query(Post).filter(Post.id == 1).first()
if post_to_update:
    post_to_update.content = "Я сегодня писала код."
    db.commit()
    print(f"\nСодержимое поста {post_to_update.title} обновлено.")

# Удаляется 1 пост
post_to_delete = db.query(Post).filter(Post.id == 2).first()
if post_to_delete:
    db.delete(post_to_delete)
    db.commit()
    print(f"\nПост с id={post_to_delete.id} удален.")

# Удаляется пользователь и все его посты
user_to_delete = db.query(User).filter(User.id == 3).first()
if user_to_delete:
    user_posts_to_delete = db.query(Post).filter(
        Post.user_id == user_to_delete.id).all()
    for post in user_posts_to_delete:
        db.delete(post)
    db.delete(user_to_delete)
    db.commit()
    print(f"\nПользователь {user_to_delete.username} и его посты удалены.")
