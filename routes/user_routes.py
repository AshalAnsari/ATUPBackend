from typing import Union
from fastapi import APIRouter, Depends, Query
from schema.user_schema import UserResponse
from schema.login_request import LoginRequest, TokenLogin
from schema.signup_request import SignupRequest
from schema.delete_request import DeleteRequest
from sqlalchemy.orm import Session
from utils.config import get_db
from controllers.user_controller import get_list_of_users, loginUser, signupUser, getUserFromToken, deleteUser

user_router = APIRouter(prefix="/users", tags=["Users"])


### ---------------- GET Request For ALL USERS ---------------- ###
@user_router.get("", response_model=list[UserResponse])
def user_list(db: Session = Depends(get_db)):
    return get_list_of_users(db)


### ---------------- POST Request For LOGIN ---------------- ###
@user_router.post("/login", response_model=Union[UserResponse,dict])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return loginUser(data.username, data.password, db)


### ---------------- POST Request For LOGIN Through Token ---------------- ###
@user_router.post("/token-login", response_model=Union[UserResponse, dict])
def token_login(data: TokenLogin, db: Session = Depends(get_db)):
    return getUserFromToken(data.token, db)


### ---------------- POST Request For SIGNUP ---------------- ###
@user_router.post("/signup", response_model=Union[UserResponse, dict])
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return signupUser(data.username, data.email, data.password, db)

@user_router.delete("/delete", response_model=dict)
def delete(token: str = Query(...), db: Session = Depends(get_db)):
    return deleteUser(token, db)