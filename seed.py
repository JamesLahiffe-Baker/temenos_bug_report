from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Website, BugReport, BugComment
from auth import get_password_hash
from datetime import datetime

#Comment out if you don't wish to seed the database with values.
def seed_database():
    db: Session = SessionLocal()
    #Seed Users
    db.add(User(
        username=f"admin",
        email=f"admin@temenos.com",
        hashed_password=get_password_hash("admin"),
        role="admin"
    ))
    db.add(User(
        username=f"regular",
        email=f"regular@temenos.com",
        hashed_password=get_password_hash("regular"),
        role="regular"
    ))
    db.add(User(
        username=f"JamesLahiffeBaker",
        email=f"james.lahiffe-baker@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"JoeCooks",
        email=f"joe.cooks@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"BillyCurry",
        email=f"billy.curry@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"KatySmith",
        email=f"katy.smith@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"AlexConnor",
        email=f"alex.connor@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"SarahCrumble",
        email=f"sarah.crumble@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"AmyWright",
        email=f"amy.wright@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.add(User(
        username=f"NeelJosh",
        email=f"neel.josh@temenos.com",
        hashed_password=get_password_hash("password"),
        role="regular"
    ))
    db.commit()

    # Seed Websites
    db.add(Website(
        name=f"People Space",
        url=f"https://peoplespace.temenos.com"
    ))
    db.add(Website(
        name=f"IT Service Desk",
        url=f"https://itservicedesk.temenos.com"
    ))
    db.add(Website(
        name=f"Uni-T",
        url=f"https://temenosgroup.sharepoint.com/sites/Uni-T"
    ))
    db.add(Website(
        name=f"EBiz",
        url=f"https://ebiz.temenosgroup.com"
    ))
    db.add(Website(
        name=f"Payroll Immedis",
        url=f"https://portal.immedis.com"
    ))
    db.add(Website(
        name=f"Yammer",
        url=f"https://engage.cloud.microsoft/main/org/temenos.com"
    ))
    db.add(Website(
        name=f"Knowledge Center",
        url=f"https://tkc.temenos.com"
    ))
    db.add(Website(
        name=f"Travel Application",
        url=f"https://travel.temenos.com"
    ))
    db.add(Website(
        name=f"T-Stars",
        url=f"https://cloud.workhuman.com/microsites/t/home?client=temenos&setCAG=false"
    ))
    db.add(Website(
        name=f"Currency Exchange",
        url=f"https://www.xe.com"
    ))
    db.commit()

    #Seed BugReports
    if db.query(BugReport).count() < 10:
        users = db.query(User).all()
        websites = db.query(Website).all()
        bug_reports = [
            {
                "title": "Login button unresponsive on homepage",
                "description": "Clicking the login button on People Space doesn't trigger any action. Tested on Chrome and Firefox.",
                "status": "Open",
                "priority": "High",
                "website": "People Space",
                "reporter": "JamesLahiffeBaker"
            },
            {
                "title": "Service desk form validation issue",
                "description": "Form accepts empty ticket descriptions on IT Service Desk. Should enforce required fields.",
                "status": "Open",
                "priority": "Medium",
                "website": "IT Service Desk",
                "reporter": "JoeCooks"
            },
            {
                "title": "Broken link in Uni-T course dashboard",
                "description": "The 'Access Materials' button leads to a 404 page in several courses.",
                "status": "In Progress",
                "priority": "High",
                "website": "Uni-T",
                "reporter": "BillyCurry"
            },
            {
                "title": "Slow load time for payroll portal",
                "description": "Immedis portal takes over 10 seconds to load after login.",
                "status": "Open",
                "priority": "Medium",
                "website": "Payroll Immedis",
                "reporter": "KatySmith"
            },
            {
                "title": "Image upload fails in Yammer threads",
                "description": "Users can't attach images in comments, error message says 'Unsupported format'.",
                "status": "Open",
                "priority": "Low",
                "website": "Yammer",
                "reporter": "AlexConnor"
            },
            {
                "title": "Navigation bar overlaps content on TKC",
                "description": "On smaller screens, the navigation bar covers the main article body.",
                "status": "Open",
                "priority": "Medium",
                "website": "Knowledge Center",
                "reporter": "SarahCrumble"
            },
            {
                "title": "Travel approval emails not being sent",
                "description": "After submitting travel requests, no confirmation or approval emails are received.",
                "status": "Open",
                "priority": "High",
                "website": "Travel Application",
                "reporter": "AmyWright"
            },
            {
                "title": "T-Stars points not updating after redeeming",
                "description": "User balance doesn’t reflect redeemed gift card, even after refresh.",
                "status": "Open",
                "priority": "Medium",
                "website": "T-Stars",
                "reporter": "NeelJosh"
            },
            {
                "title": "Currency conversion tool displays incorrect rates",
                "description": "Displayed exchange rates lag behind real-time rates by 15–20 minutes.",
                "status": "In Progress",
                "priority": "Low",
                "website": "Currency Exchange",
                "reporter": "JamesLahiffeBaker"
            },
            {
                "title": "No error message when password is incorrect",
                "description": "The login form on EBiz does nothing when incorrect credentials are entered.",
                "status": "Open",
                "priority": "High",
                "website": "EBiz",
                "reporter": "JoeCooks"
            },
        ]
        for bug in bug_reports:
            website = db.query(Website).filter(Website.name == bug["website"]).first()
            reporter = db.query(User).filter(User.username == bug["reporter"]).first()
            report = BugReport(
                title=bug["title"],
                description=bug["description"],
                status=bug["status"],
                priority=bug["priority"],
                website_id=website.website_id,
                reported_by_user_id=reporter.user_id,
                reported_at=datetime.utcnow()
            )
            db.add(report)
        db.commit()

    #Seed BugComments
    if db.query(BugComment).count() < 10:
        bugs = db.query(BugReport).all()
        users = db.query(User).all()
        comments = [
            "Thanks, we'll investigate this shortly.",
            "Can you confirm the browser and OS used?",
            "Issue replicated. Raising a ticket with dev team.",
            "Looks like a regression from last week's patch.",
            "Try clearing your cache and reloading—still happens?",
            "We’ve deployed a fix, please retest.",
            "Not reproducible on staging. Can you retry?",
            "Confirmed. UX team has been alerted.",
            "Thanks for the detailed report, very helpful!",
            "We're working on a hotfix, ETA tomorrow."
        ]
        for i in range(10):
            comment = BugComment(
                bug_id=bugs[i].bug_id,
                comment=comments[i],
                created_by_user_id=users[i % len(users)].user_id
            )
            db.add(comment)
        db.commit()
    db.close()
