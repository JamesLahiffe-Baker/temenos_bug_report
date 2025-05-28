print("[INFO] Loading dashboard_controller module...")

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Website, BugReport
from fastapi.templating import Jinja2Templates

print("[INFO] Imported all required modules in dashboard_controller")
print("[INFO] Initialising auth_controller in dashboard_controller...")

templates = Jinja2Templates(directory="templates")
router = APIRouter()

from controllers.auth_controller import sessions
print("[INFO] Imported session management from auth_controller in dashboard_controller")

#Displays the main dashboard landing page
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
        request: Request,
        db: Session = Depends(get_db)
):
    print("[INFO] /dashboard route accessed")
    user_id = sessions.get("user")
    if not user_id:
        print("[WARN] No user session found, redirecting to login")
        return RedirectResponse("/", status_code=303)
    user = db.query(User).get(user_id)
    websites = db.query(Website).all()
    bugs = db.query(BugReport).all()
    print(f"[SUCCESS] Dashboard loaded for user_id: {user_id} | Username: {user.username}")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "websites": websites,
        "bugs": bugs
    })
