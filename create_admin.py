from database import SessionLocal
from services.auth_service import create_user

db = SessionLocal()

create_user(
    db,
    "admin",
    "finpilot123",
    "Prasanna"
)

db.close()

print("Admin account created.")