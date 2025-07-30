from typing import Union
from fastapi import APIRouter, Depends
from schema.activity_request import ActivityRequest, UserActivity
from sqlalchemy.orm import Session
from utils.config import get_db
from controllers.activity_controller import add_new_activity, get_all_activity_for_a_user

activity_router = APIRouter(prefix="/activity", tags=["Activity"])

### -------------- POST Request For Adding New Activity ---------------- ###
@activity_router.post("/add_acitivity", response_model=dict)
def addActivity(data: ActivityRequest, db: Session = Depends(get_db)):
    return add_new_activity(data.token, data.action, db)


### -------------- POST Request For Fetching User Activities ---------------- ###
@activity_router.post("/get_user_activity", response_model=dict)
def getActivity(data: UserActivity, db: Session = Depends(get_db)):
    return get_all_activity_for_a_user(data.token, db)