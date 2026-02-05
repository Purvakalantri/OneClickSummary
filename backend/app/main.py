from fastapi import FastAPI
from app.routes import meeting, dashboard, user_dashboard, manager_dashboard, manager_actions, users, user_actions

app = FastAPI()

app.include_router(meeting.router)
app.include_router(dashboard.router)
app.include_router(user_dashboard.router)
app.include_router(manager_dashboard.router)
app.include_router(manager_actions.router)
app.include_router(users.router)
app.include_router(user_actions.router)



@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }