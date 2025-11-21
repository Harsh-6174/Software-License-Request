from fastapi import FastAPI
from .user_verification import user_exists

app = FastAPI()

@app.get("/check-user")
def check_user(employee_id : str):
    return {
        "exists" : user_exists(employee_id)
    }