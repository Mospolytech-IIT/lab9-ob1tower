"""
Лабораторная работа №9: Работа с базой данных через SQLAlchemy.
"""
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, User, Post

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание экземпляра FastAPI
app = FastAPI()

def get_db():
    """
    Определяется зависимость.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    """
    Получения веб-приложения.
    """
    return FileResponse("public/index.html")

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    """
    Получения списка пользователей.
    """
    return db.query(User).all()

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о пользователе по ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return user

@app.post("/users")
def create_user(username: str = Body(), email: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    """
    Добавление пользователя.
    """
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = Body(), email: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    """
    Обновление пользователя.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удаления пользователя.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удален."}

@app.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    """
    Получения списка поста.
    """
    return db.query(Post).all()

@app.get("/posts/{post_id}")
def read_post(post_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о посте по ID.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден.")
    return post

@app.post("/posts")
def create_post(title: str = Body(), content: str = Body(), user_id: int = Body(), db: Session = Depends(get_db)):
    """
    Добавление поста.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str = Body(), content: str = Body(), db: Session = Depends(get_db)):
    """
    Обновления поста.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден.")
    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Удаления поста.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден.")
    db.delete(post)
    db.commit()
    return {"message": "Пост удален."}
