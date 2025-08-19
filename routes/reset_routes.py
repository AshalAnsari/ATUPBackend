from fastapi import APIRouter, Depends
from utils.config import get_db
from schema.reset_schema import ResetSchema, OTPSchema
from sqlalchemy.orm import Session
from controllers.user_controller import sendResetPasswordOTP, checkOTP

reset_router = APIRouter(prefix="/atup-reset", tags=["reset"])


@reset_router.post("/send-otp", response_model=dict)
def send_otp_to_user(data: ResetSchema, db: Session = Depends(get_db)):
    return sendResetPasswordOTP(data.email, db)


@reset_router.post("/check-otp", response_model=dict)
def validateOTP(data: OTPSchema, db : Session = Depends(get_db)):
    return checkOTP(data.otp, db)
