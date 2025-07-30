import uuid
from models.activity_model import ActivityModel
from sqlalchemy.orm import Session
from schema.activity_request import ActivityResponse
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

def add_new_activity(token: str, action: str, db: Session):
    if token is None or token == "" or action is None or action == "":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error':"Missing Token or Action"
            }
        )
    
    new_activity = ActivityModel(
        id = str(uuid.uuid4()),
        user_id = token,
        action = action
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message':'Activity created!',
            'action':new_activity.action,
            'timestamp':new_activity.timestamp.isoformat()
        }
    )

def get_all_activity_for_a_user(token: str, db: Session):
    if token is None or token == "":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'error':'Your are not authorized!'
            }      
        )
    
    user_activity = db.query(ActivityModel).filter_by(user_id = token).all()

    if len(user_activity) > 0:
        return {
            'id':token,
            'activity':[
                ActivityResponse(action=act.action, timestamp=act.timestamp).model_dump()
                for act in user_activity
            ]
        }
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error':'No activity found!'
        }
    )

def deleteAllActivityForAUser(token: str, db: Session):
    if token == "" or token is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error':"Missing token! Cannot delete any activity!"
            }
        )

    activity_to_delete = db.query(ActivityModel).filter_by(user_id = token).delete()

    does_activity_exist = db.query(ActivityModel).filter_by(user_id = token).first()

    if does_activity_exist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'error':"Couldn't delete the user's activities"
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message':'Activites deleted',
            'activities':activity_to_delete
        }
    )

