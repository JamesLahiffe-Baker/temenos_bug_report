from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Website, BugReport, BugComment
from auth import get_password_hash
from datetime import datetime

#Comment out if you don't wish to seed the database with values.
def seed_database():
    db: Session = SessionLocal()
    #Seed Users
    users=[
        {
            "username": "admin",
            "email": "admin@temenos.com",
            "password": "admin",
            "role": "admin"
        },
        {
            "username": "regular",
            "email": "regular@temenos.com",
            "password": "regular",
            "role": "regular"
        },
        {
            "username": "JamesLahiffeBaker",
            "email": "james.lahiffe-baker@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "JoeCooks",
            "email": "joe.cooks@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "BillyCurry",
            "email": "billy.curry@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "KatySmith",
            "email": "katy.smith@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "AlexConnor",
            "email": "alex.connor@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "SarahCrumble",
            "email": "sarah.crumble@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "AmyWright",
            "email": "amy.wright@temenos.com",
            "password": "password",
            "role": "regular"
        },
        {
            "username": "NeelJosh",
            "email": "neel.josh@temenos.com",
            "password": "password",
            "role": "regular"
        }
    ]
    for user in users:
        db.add(User(
            username=user["username"],
            email=user["email"],
            hashed_password=get_password_hash(user["password"]),
            role=user["role"]
        ))
    db.commit()

    # Seed Websites
    websites = [
        {
            "name": "People Space",
            "url": "https://peoplespace.temenos.com"
        },
        {
            "name": "IT Service Desk",
            "url": "https://itservicedesk.temenos.com"
        },
        {
            "name": "Uni-T",
            "url": "https://temenosgroup.sharepoint.com/sites/Uni-T"
        },
        {
            "name": "EBiz",
            "url": "https://ebiz.temenosgroup.com"
        },
        {
            "name": "Payroll Immedis",
            "url": "https://portal.immedis.com"
        },
        {
            "name": "Yammer",
            "url": "https://engage.cloud.microsoft/main/org/temenos.com"
        },
        {
            "name": "Knowledge Center",
            "url": "https://tkc.temenos.com"
        },
        {
            "name": "Travel Application",
            "url": "https://travel.temenos.com"
        },
        {
            "name": "T-Stars",
            "url": "https://cloud.workhuman.com/microsites/t/home?client=temenos&setCAG=false"
        },
        {
            "name": "Currency Exchange",
            "url": "https://www.xe.com"
        }
    ]
    for website in websites:
        db.add(Website(
            name=website["name"],
            url=website["url"]
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
                "reporter": "JoeCooks"
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
                "reporter": "AmyWright"
            },
            {
                "title": "Image upload fails in Yammer threads",
                "description": "Users can't attach images in comments, error message says 'Unsupported format'.",
                "status": "Open",
                "priority": "Low",
                "website": "IT Service Desk",
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
                "reporter": "NeelJosh"
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
            db.add(BugReport(
                title=bug["title"],
                description=bug["description"],
                status=bug["status"],
                priority=bug["priority"],
                website_id=website.website_id,
                reported_by_user_id=reporter.user_id,
                reported_at=datetime.utcnow()
            ))
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
