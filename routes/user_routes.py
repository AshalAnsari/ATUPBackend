from typing import Union
from fastapi import APIRouter, Depends, Query
from schema.user_schema import UserResponse
from schema.login_request import LoginRequest, TokenLogin
from schema.signup_request import SignupRequest
from schema.delete_request import DeleteRequest
from schema.GoogleSigin import GoogleSigninSchema, LoggingGoogleSigninSchema
from schema.edit_request import EditRequest
from sqlalchemy.orm import Session
from utils.config import get_db
from controllers.user_controller import get_list_of_users, loginUser, signupUser, getUserFromToken, deleteUser, editUserDetails, verify_email, signupWithGoogle

user_router = APIRouter(prefix="/users", tags=["Users"])


### ---------------- GET Request For ALL USERS ---------------- ###
@user_router.get("", response_model=list[UserResponse])
def user_list(db: Session = Depends(get_db)):
    return get_list_of_users(db)


### ---------------- ATUP Basic Operational APIs ---------------- ###
@user_router.post("/login", response_model=Union[UserResponse,dict])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return loginUser(data.username, data.password, db)


@user_router.post("/token-login", response_model=Union[UserResponse, dict])
def token_login(data: TokenLogin, db: Session = Depends(get_db)):
    return getUserFromToken(data.token, db)


@user_router.post("/signup", response_model=Union[UserResponse, dict])
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return signupUser(data.username, data.email, data.password, db)

@user_router.delete("/delete", response_model=dict)
def delete(token: str = Query(...), db: Session = Depends(get_db)):
    return deleteUser(token, db)

@user_router.put("/edit", response_model=dict)
def edit(data: EditRequest, token: str = Query(...), db: Session = Depends(get_db)):
    return editUserDetails(token, data.model_dump(exclude_unset=True), db)


#### --------------------- Email Verification Methods -------------------------########
@user_router.get("/verify-email", response_class=dict)
def verify(token: str = Query(...), db: Session = Depends(get_db)):
    return verify_email(token, db)

#### --------------------- Google Sigin Methods -------------------------########
@user_router.post("/signup/google", response_model=Union[UserResponse, dict])
def signup_google(data: GoogleSigninSchema, db: Session = Depends(get_db)):
    return signupWithGoogle(data.token, data.username, data.email, data.image, db)