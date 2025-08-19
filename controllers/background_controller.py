from sqlalchemy.orm import Session
from utils.config import SessionLocal
from datetime import datetime, timedelta, UTC
from models.user_model import User
from apscheduler.schedulers.background import BackgroundScheduler
from models.reset_model import ResetModel

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



def deleteExpiredOTP():
    print("---------------- Beginning Background Task For OTP Deletion ----------------")
    db: Session = SessionLocal()
    now = datetime.now(UTC)
    print(now)

    # Delete OTPs that are either expired OR already used
    reset_entries = db.query(ResetModel).filter(
        (ResetModel.is_used == True) | (ResetModel.expires_at <= now)
    ).delete(synchronize_session=False)

    print("Deleted Entries: ", reset_entries)

    db.commit()
    db.close()
    print(" ---------- Ending Background Task For OTP Deletion ---------------- ")



def startScheduler():
    print("------- Background Scheduler has started! --------")
    scheduler = BackgroundScheduler()
    scheduler.add_job(deleteUnVerifiedUsers, "interval", days=1)
    scheduler.add_job(deleteExpiredOTP, "interval", minutes=10)
    scheduler.start()
