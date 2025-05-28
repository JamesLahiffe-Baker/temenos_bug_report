print("[INFO] Loading bug_controller module...")

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import BugReport, BugComment, Website, User
from fastapi.templating import Jinja2Templates

print("[INFO] Imported all required modules in bug_controller")
print("[INFO] Initialising auth_controller in bug_controller...")

templates = Jinja2Templates(directory="templates")
router = APIRouter()

from controllers.auth_controller import sessions
print("[INFO] Imported session management from auth_controller in bug_controller")

#Displays the "Report a Bug" form
@router.get("/report_bug", response_class=HTMLResponse)
def report_bug_form(
        request: Request,
        db: Session = Depends(get_db)
):
    print("[INFO] GET /report_bug accessed")
    user_id = sessions.get("user")
    if not user_id:
        print("[WARN] No user session found, redirecting to login")
        return RedirectResponse("/", status_code=303)
    user = db.query(User).get(user_id)
    websites = db.query(Website).all()
    print(f"[SUCCESS] Report bug form rendered for user {user.username}")
    return templates.TemplateResponse("report_bug.html", {
        "request": request,
        "user": user,
        "websites": websites
    })

#Submits a new bug report
@router.post("/report_bug")
def report_bug(
        title: str = Form(...),
        description: str = Form(...),
        website_id: int = Form(...),
        priority: str = Form(...),
        db: Session = Depends(get_db)
):
    print("[INFO] POST /report_bug submitted")
    try:
        user_id = sessions.get("user")
        if not user_id:
            print("[WARN] Bug submission attempt without session")
            return RedirectResponse("/", status_code=303)
        #Create and persist bug report
        bug = BugReport(
            title=title,
            description=description,
            website_id=website_id,
            reported_by_user_id=user_id,
            priority=priority
        )
        db.add(bug)
        db.commit()
        print(f"[SUCCESS] Bug reported by user_id {user_id}: {title}")
        return RedirectResponse("/bugs", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to report bug: {str(e)}")
        return templates.TemplateResponse("dashboard.html", {
            "request": {},
            "error": f"Failed to report bug: {str(e)}"
        })

#Displays the bug tracker with filters and sorting
@router.get("/bugs", response_class=HTMLResponse)
def bug_tracker(
        request: Request,
        status: str = None,
        priority: str = None,
        sort: str = "newest",
        db: Session = Depends(get_db)
):
    print("[INFO] GET /bugs accessed")
    user_id = sessions.get("user")
    if not user_id:
        print("[WARN] Unauthorized access to /bugs")
        return RedirectResponse("/", status_code=303)
    user = db.query(User).get(user_id)
    query = db.query(BugReport)
    #Filter by status and priority if specified
    if status:
        query = query.filter(BugReport.status == status)
    if priority:
        query = query.filter(BugReport.priority == priority)
    #Sort by reported date
    bugs = query.order_by(BugReport.reported_at.desc() if sort == "newest" else BugReport.reported_at.asc()).all()
    print(f"[SUCCESS] Bug tracker loaded for {user.username}, filters applied: status={status}, priority={priority}, sort={sort}")
    return templates.TemplateResponse("bug_tracker.html", {
        "request": request,
        "user": user,
        "bugs": bugs,
        "filter_status": status,
        "filter_priority": priority,
        "sort_order": sort
    })

#Displays a single bug's detail view
@router.get("/bugs/{bug_id}", response_class=HTMLResponse)
def bug_details(
        bug_id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    print(f"[INFO] GET /bugs/{bug_id} accessed")
    user_id = sessions.get("user")
    user = db.query(User).get(user_id)
    bug = db.query(BugReport).get(bug_id)
    print(f"[SUCCESS] Bug details page loaded for bug #{bug_id} by user_id {user_id}")
    return templates.TemplateResponse("bug_details.html", {
        "request": request,
        "user": user,
        "bug": bug
    })

#Adds a comment to a bug
@router.post("/bugs/{bug_id}/comment")
def add_comment(
        bug_id: int,
        comment: str = Form(...),
        db: Session = Depends(get_db)
):
    print(f"[INFO] POST /bugs/{bug_id}/comment submitted")
    try:
        user_id = sessions.get("user")
        if not user_id:
            print("[WARN] Unauthorized comment attempt")
            return RedirectResponse("/", status_code=303)
        new_comment = BugComment(
            bug_id=bug_id,
            comment=comment,
            created_by_user_id=user_id
        )
        db.add(new_comment)
        db.commit()
        print(f"[SUCCESS] Comment added to bug #{bug_id} by user_id {user_id}")
        return RedirectResponse(f"/bugs/{bug_id}", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to add comment: {str(e)}")
        return templates.TemplateResponse("bug_details.html", {
            "request": {},
            "error": f"Failed to add comment: {str(e)}"
        })

#Updates the bug's status and priority(admin only)
@router.post("/bugs/{bug_id}/update")
def update_bug(
        bug_id: int,
        status: str = Form(...),
        priority: str = Form(...),
        db: Session = Depends(get_db)
):
    print(f"[INFO] POST /bugs/{bug_id}/update submitted")
    user_id = sessions.get("user")
    user = db.query(User).get(user_id)
    if not user or user.role != "admin":
        print("[WARN] Non-admin attempted to update bug")
        return RedirectResponse("/dashboard", status_code=303)
    bug = db.query(BugReport).get(bug_id)
    bug.status = status
    bug.priority = priority
    db.commit()
    print(f"[SUCCESS] Bug #{bug_id} updated by admin {user.username}")
    return RedirectResponse(f"/bugs/{bug_id}", status_code=303)
