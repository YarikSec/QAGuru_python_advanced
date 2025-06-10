from fastapi import FastAPI, HTTPException, Header, Depends
import uvicorn
import json


from pydantic import BaseModel
from typing import Optional, List

from models.AppStatus import AppStatus
from models.User import User


app = FastAPI()

class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class SupportData(BaseModel):
    url: str
    text: str

class ResponseModel(BaseModel):
    data: UserData
    support: SupportData

class UserCreate(BaseModel):
    name: str
    job: str

class UserResponse(BaseModel):
    name: str
    job: str
    id: Optional[str] = None
    createdAt: Optional[str] = None

class LoginData(BaseModel):
    email: str
    password: Optional[str] = None

# Mock data
users = {
    2: {
        "id": 2,
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "https://reqres.in/img/faces/2-image.jpg",
    },
    3: {
        "id": 3,
        "email": "emma.wong@reqres.in",
        "first_name": "Emma",
        "last_name": "Wong",
        "avatar": "https://reqres.in/img/faces/3-image.jpg",
    },
    4: {
        "id": 4,
        "email": "eve.holt@reqres.in",
        "first_name": "Eve",
        "last_name": "Holt",
        "avatar": "https://reqres.in/img/faces/4-image.jpg",
    }
}

support_info = {
    "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
    "text": "Tired of writing endless social media content? Let Content Caddy generate it for you.",
}

def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != "reqres-free-v1":
        raise HTTPException(status_code=403, detail="Missing API key.")
    return x_api_key

@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_user(user_id: int, api_key: str = Depends(verify_api_key)):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user, "support": support_info}

@app.post("/api/", response_model=UserResponse)
def create_user(user: UserCreate, api_key: str = Depends(verify_api_key)):
    return {"name": user.name, "job": user.job, "id": "1", "createdAt": "2023-11-14T12:00:00.000Z"}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, api_key: str = Depends(verify_api_key)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}

@app.post("/api/login")
def login(login_data: LoginData):
    if not login_data.password:
        raise HTTPException(status_code=400, detail="Missing password")
    return {"token": "QpwL5tke4Pnpja7X4"}

@app.get("/api/users")
def get_users(page: int = 1):
    if page == 2:
        return {
            "data": [
                {"id": 7, "email": "michael.lawson@reqres.in", "first_name": "Michael", "last_name": "Lawson", "avatar": "https://reqres.in/img/faces/7-image.jpg"},
                {"id": 8, "email": "lindsay.ferguson@reqres.in", "first_name": "Lindsay", "last_name": "Ferguson", "avatar": "https://reqres.in/img/faces/8-image.jpg"}
            ]
        }
    return {"data": list(users.values())}

# To run this app, use the following command in your terminal:
# uvicorn filename:app --reload

if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="localhost", port=8002)