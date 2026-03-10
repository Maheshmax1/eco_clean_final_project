import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal
import models
import crud

def create_admin():
    db = SessionLocal()
    try:
        admin_email = "admin@ecoclean.com"
        # Check if user already exists
        db_user = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if db_user:
            # Update existing user to admin and reset password
            db_user.role = "admin"
            db_user.hashed_password = crud.get_password_hash("admin123")
            db.commit()
            print(f"Updated existing user {admin_email} to admin role and reset password to admin123.")
        else:
            # Create new admin user
            hashed_password = crud.get_password_hash("admin123")
            new_admin = models.User(
                full_name="System Admin",
                email=admin_email,
                phone="0000000000",
                hashed_password=hashed_password,
                role="admin"
            )
            db.add(new_admin)
            db.commit()
            print(f"Created new admin user: {admin_email} with password: admin123")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
