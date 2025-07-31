import uuid
from models.user_model import User
from schema.user_schema import UserResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status
from controllers.activity_controller import deleteAllActivityForAUser
from datetime import datetime
from views.email import send_verification_email

def get_list_of_users(db: Session) -> list[UserResponse]:
    users = db.query(User).all()
    return [UserResponse.model_validate(user) for user in users]

def getUserFromToken(token: str, db: Session):
    if token == "" or token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error':"You are not authorized!"
            }
        )

    existing_user = db.query(User).filter((User.id == token)).first()

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'token':existing_user.id,
                'username':existing_user.username,
                'email':existing_user.email,
                'image': existing_user.image,
                'verified': existing_user.verified,
                'createdOn':existing_user.createdOn.isoformat()
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error':"User not found!"
        }
    )

def loginUser(username: str, password: str, db: Session):
    if username == "" or password == "":
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'error':"Username or Password is missing!"}
            )
    
    ### Now, to Authenticate the user ###
    existing_user = db.query(User).filter((User.username == username) & (User.password == password)).first()

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'token': existing_user.id,
                'username': existing_user.username,
                'email': existing_user.email,
                'image': existing_user.image,
                'verified': existing_user.verified,
                'createdOn': existing_user.createdOn.isoformat()
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': "Incorrect Username or Password"
        }
    )

def signupUser(username: str, email: str, password: str, db: Session):
    if(username == "" or email == "" or password == ""):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error': "Username, Email, or Password is missing!"
            }
        )
    
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_302_FOUND,
            content={
                'error': 'User already exist!'
            }   
        )
    
    
    new_user = User(
        id = str(uuid.uuid4()),
        username = username,
        email = email,
        password = password,
        image = None,
        verified = False,
    )

    send_verification_email(email, new_user.id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'token': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'image': new_user.image,
            'verified': new_user.verified,
            'createdOn': new_user.createdOn.isoformat(),
            'message': "An email verification has been sent to you email. Verify in 2 days, otherwise your account will be deleted!"
        }
    )

def deleteUser(token: str, db: Session):
    if not token:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': "Missing token!"}
        )

    # Fetch user before deletion for possible return
    user_to_delete = db.query(User).filter_by(id=token).first()

    if not user_to_delete:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'error': "User not found"}
        )

    # Save info to return, then delete
    user_data = {
        "id": str(user_to_delete.id),
        "username": user_to_delete.username,
        "email": user_to_delete.email,
        "createdOn": str(user_to_delete.createdOn.isoformat()),  # convert datetime to string
        # exclude or serialize any other fields
    }

    db.delete(user_to_delete)
    db.commit()

    deleteAllActivityForAUser(token, db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message': 'User deleted successfully!',
            'user': user_data
        }
    )

def editUserDetails(token: str, data: dict, db: Session):
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'error': "You are not authorized"}
        )
    
    user = db.query(User).filter_by(id=token).first()

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': "User doesn't exist or not found!"}
        )

    for key, value in data.items():
        if hasattr(user, key):
            attr_type = type(getattr(user, key))
            if attr_type is datetime and isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    return JSONResponse(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={'error': f"Invalid datetime format for '{key}'"}
                    )
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {
        'message':"User updated successfully",
        'token':user.id,
        'username': user.username,
        'email': user.email,
        'image': user.image,
        'verified': user.verified,
    }

def verify_email(token: str, db: Session):
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'error': "You are not authorized"}
        )

    user = db.query(User).filter_by(id = token).first()

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': "User not found!"}
        )

    user.verified = True
    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User Verified!",
        }
    )
