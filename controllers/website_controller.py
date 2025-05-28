print("[INFO] Loading website_controller module...")

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Website, User
from fastapi.templating import Jinja2Templates

print("[INFO] Imported all required modules in website_controller")
print("[INFO] Initialising auth_controller in website_controller...")

templates = Jinja2Templates(directory="templates")
router = APIRouter()

from controllers.auth_controller import sessions
print("[INFO] Imported session management from auth_controller in website_controller")

#View all managed websites(admin)
@router.get("/manage_websites", response_class=HTMLResponse)
def manage_websites(
        request: Request,
        db: Session = Depends(get_db)
):
    print("[INFO] Accessing /manage_websites")
    user_id = sessions.get("user")
    user = db.query(User).get(user_id)
    #Redirect non-admins to dashboard
    if not user or user.role != "admin":
        print("[WARN] Unauthorized access attempt to /manage_websites")
        return RedirectResponse("/dashboard", status_code=303)
    websites = db.query(Website).all()
    print(f"[INFO] Retrieved {len(websites)} websites")
    return templates.TemplateResponse("manage_websites.html", {
        "request": request,
        "user": user,
        "websites": websites
    })

#Add a new website to manage(admin)
@router.post("/manage_websites/add")
def add_website(
        name: str = Form(...),
        url: str = Form(...),
        db: Session = Depends(get_db)
):
    print(f"[INFO] Attempting to add new website: {name} ({url})")
    try:
        user_id = sessions.get("user")
        user = db.query(User).get(user_id)
        #Verify admin permission
        if not user or user.role != "admin":
            print("[WARN] Non-admin user tried to add a website")
            return RedirectResponse("/dashboard", status_code=303)
        #Create and persist the new website entry
        website = Website(name=name, url=url)
        db.add(website)
        db.commit()
        print(f"[SUCCESS] Website '{name}' added")
        return RedirectResponse("/manage_websites", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to add website: {str(e)}")
        return templates.TemplateResponse("manage_websites.html", {
            "request": {},
            "error": f"Error adding website: {str(e)}"
        })

#Delete a website(admin)
@router.post("/delete_website/{website_id}")
def delete_website(
        website_id: int,
        db: Session = Depends(get_db)
):
    print(f"[INFO] Attempting to delete website ID {website_id}")
    try:
        user_id = sessions.get("user")
        user = db.query(User).get(user_id)
        #Prevent non-admin access
        if not user or user.role != "admin":
            print("[WARN] Non-admin attempted to delete a website")
            return RedirectResponse("/dashboard", status_code=303)
        website = db.query(Website).get(website_id)
        if website:
            db.delete(website)
            db.commit()
            print(f"[SUCCESS] Website ID {website_id} deleted")
        else:
            print(f"[WARN] Website ID {website_id} not found")
        return RedirectResponse("/manage_websites", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to delete website: {str(e)}")
        return templates.TemplateResponse("manage_websites.html", {
            "request": {},
            "error": f"Error deleting website: {str(e)}"
        })
