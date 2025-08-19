from fastapi import FastAPI
from routes.user_routes import user_router
from routes.activity_routes import activity_router
from routes.reset_routes import reset_router
from controllers.background_controller import startScheduler

app = FastAPI()

startScheduler()

### ------- APP Routes --------- ###
app.include_router(user_router)
app.include_router(activity_router)
app.include_router(reset_router)

### ------------ APP Check --------------- ###
@app.get("/")
def health_check():
    return {"message": "Server is working"}