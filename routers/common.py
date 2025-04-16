
from app.db.database import SessionLocal

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create(data, db):
    db.add(data)
    db.commit()
    db.refresh(data)
    if not data:
        return None
    return data
    