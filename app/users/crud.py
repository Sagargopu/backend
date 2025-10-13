from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # In a real app, you'd hash the password here. We will add this in the final security phase.
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, 
        full_name=user.full_name, 
        role=user.role
        # hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def onboard_user(db: Session, user: schemas.UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return None # User already exists
    
    db_user = create_user(db=db, user=user)
    # In a real app, generate a unique token and store it, then email it.
    invite_token = "FAKE_INVITE_TOKEN_FOR_" + str(db_user.id)
    return {"user": db_user, "invite_token": invite_token}

def set_user_password(db: Session, user_id: int, new_password: str, token: str):
    # In the final security phase, this would verify the token and hash the password.
    # For now, we'll just simulate success.
    db_user = get_user(db, user_id)
    if db_user and token.startswith("FAKE_INVITE_TOKEN_FOR_"):
        # db_user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def get_talent_pool(db: Session, role: str | None = None, available: bool | None = None, skip: int = 0, limit: int = 100):
    query = db.query(models.User)
    if role:
        query = query.filter(models.User.role == role)
    # For now, 'available' is a placeholder. Real availability would check assignments.
    # if available is not None:
    #     query = query.filter(models.User.is_available == available)
    return query.offset(skip).limit(limit).all()

def activate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
    return db_user

def deactivate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
    return db_user



