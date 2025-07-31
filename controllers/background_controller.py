from sqlalchemy.orm import Session
from utils.config import SessionLocal
from datetime import datetime, timedelta, UTC
from models.user_model import User
from apscheduler.schedulers.background import BackgroundScheduler

def deleteUnVerifiedUsers():
    print("---------------- Begining Background Task ----------------")
    db: Session = SessionLocal()
    print(datetime.now(UTC))
    cutoff_time = datetime.now(UTC) - timedelta(days=2)
    users = db.query(User).filter(
        User.verified == False,
        User.createdOn <= cutoff_time
    ).delete()

    print("Users: ", users)

    db.commit()
    db.close()

    print(" ---------- Ending Background Task ---------------- ")

def startScheduler():
    print("------- Background Scheduler has started! --------")
    scheduler = BackgroundScheduler()
    scheduler.add_job(deleteUnVerifiedUsers, "interval", days=1)
    scheduler.start()
