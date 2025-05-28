print("[INFO] Loading user_controller module...")

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from fastapi.templating import Jinja2Templates

print("[INFO] Imported all required modules in user_controller")
print("[INFO] Initialising auth_controller in user_controller...")

templates = Jinja2Templates(directory="templates")
router = APIRouter()

from controllers.auth_controller import sessions
print("[INFO] Imported session management from auth_controller in user_controller")

#View all users and perform user management(admin only)
@router.get("/manage_users", response_class=HTMLResponse)
def manage_users(
        request: Request,
        db: Session = Depends(get_db)
):
    print("[INFO] Accessing /manage_users")
    current_user_id = sessions.get("user")
    current_user = db.query(User).get(current_user_id)
    #Ensure only admins can access
    if not current_user or current_user.role != "admin":
        print("[WARN] Unauthorized access to /manage_users")
        return RedirectResponse("/dashboard", status_code=303)
    users = db.query(User).all()
    print(f"[INFO] Loaded {len(users)} users for management")
    return templates.TemplateResponse("manage_users.html", {
        "request": request,
        "user": current_user,
        "users": users
    })

#Promote a regular user to admin(admin only)
@router.post("/make_admin/{user_id}")
def make_admin(
        user_id: int,
        db: Session = Depends(get_db)
):
    print(f"[INFO] Attempting to promote user {user_id} to admin")
    current_user_id = sessions.get("user")
    current_user = db.query(User).get(current_user_id)
    #Prevent non-admins from promoting users
    if not current_user or current_user.role != "admin":
        print("[WARN] Unauthorized attempt to promote user")
        return RedirectResponse("/dashboard", status_code=303)
    user = db.query(User).get(user_id)
    if user:
        user.role = "admin"
        db.commit()
        print(f"[SUCCESS] User {user_id} promoted to admin")
    return RedirectResponse("/manage_users", status_code=303)

#Delete a regular user(admin only)
@router.post("/delete_user/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    print(f"[INFO] Attempting to delete user {user_id}")
    current_user_id = sessions.get("user")
    current_user = db.query(User).get(current_user_id)
    #Block deletion if not admin
    if not current_user or current_user.role != "admin":
        print("[WARN] Unauthorized attempt to delete user")
        return RedirectResponse("/dashboard", status_code=303)
    user = db.query(User).get(user_id)
    #Prevent deletion of fellow admins
    if user and user.role != "admin":
        db.delete(user)
        db.commit()
        print(f"[SUCCESS] User {user_id} deleted")
    else:
        print(f"[WARN] Attempted to delete admin user {user_id}, which is not allowed")
    return RedirectResponse("/manage_users", status_code=303)
