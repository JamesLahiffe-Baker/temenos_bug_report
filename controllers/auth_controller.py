print("[INFO] Loading auth_controller module...")

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import get_password_hash, verify_password
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates

print("[INFO] Imported all required modules in auth_controller")
print("[INFO] Initialising auth_controller...")

templates = Jinja2Templates(directory="templates")
router = APIRouter()
sessions = {}

print("[INFO] Initialising auth_controller done")

#Displays the login page
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    print("[INFO] Rendering login page")
    return templates.TemplateResponse("login.html", {
        "request": request
    })

#Displays the user registration form
@router.get("/register", response_class=HTMLResponse)
def register_form(
        request: Request,
        db: Session = Depends(get_db)
):
    print("[INFO] Accessed registration form")
    user_exists = db.query(User).first() is not None
    message = None
    #First user gets admin privileges
    if not user_exists:
        message = (
            "You are the first user. You shall become the admin of this site."
            "All other users will become regular users unless you alter their privileges."
        )
        print("[INFO] First user detected – assigning admin role suggestion")
    return templates.TemplateResponse("register.html", {
        "request": request,
        "message": message
    })

#Handles new user registration
@router.post("/register")
def register(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    print(f"[INFO] Attempting registration for user: {username}")
    try:
        #Check for existing username
        if db.query(User).filter(User.username == username).first():
            print("[WARN] Username already taken")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "That username is already taken. Please choose another."
            })
        #Check for existing email
        if db.query(User).filter(User.email == email).first():
            print("[WARN] Email already registered")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "That email is already registered. Please log in instead."
            })
        hashed = get_password_hash(password)
        user = User(username=username, email=email, hashed_password=hashed)
        #First user gets admin role
        if not db.query(User).first():
            user.role = "admin"
            print("[INFO] First user registered – assigning admin role")
        db.add(user)
        db.commit()
        print(f"[SUCCESS] Registered new user: {username}")
        return RedirectResponse("/", status_code=303)
    except IntegrityError:
        db.rollback()
        print("[ERROR] Integrity error during registration")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "That email is already in use. Try logging in instead."
        })
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Unexpected registration error: {str(e)}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Unexpected error occurred. Please try again or contact support."
        })

#Handles login logic and sets session
@router.post("/login")
def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    print(f"[INFO] Login attempt by: {username}")
    try:
        user = db.query(User).filter(User.username == username).first()
        #Validate credentials
        if not user or not verify_password(password, user.hashed_password):
            print("[WARN] Invalid login credentials")
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Invalid credentials"
            })
        #Save session in memory
        sessions["user"] = user.user_id
        print(f"[SUCCESS] User {username} logged in")
        return RedirectResponse("/dashboard", status_code=303)
    except Exception as e:
        print(f"[ERROR] Login failed: {str(e)}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"Login failed: {str(e)}"
        })

#Logs out the user and clears session
@router.get("/logout")
def logout():
    print("[INFO] User logged out")
    sessions.pop("user", None)
    return RedirectResponse("/", status_code=303)
