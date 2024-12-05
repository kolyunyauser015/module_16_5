from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "users": users}
    )


@app.get("/users/{user_id}", response_model=List[User])
async def get_user(
        request: Request,
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)]):
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "user": users[user_id - 1]}
    )


@app.post("/user/{username}/{age}", response_model=User)
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=12, le=120, description="Enter age", example=24)]
):
    new_id = max((ur.id for ur in users), default=0) + 1
    new_user = User(id=new_id,
                    username=username,
                    age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=12, le=120, description="Enter age", example=24)]
):
    for ur in users:
        if ur.id == user_id:
            ur.username = username
            ur.age = age
            return ur
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)]
):
    for i, ur in enumerate(users):
        if ur.id == user_id:
            del users[i]
            return ur
    raise HTTPException(status_code=404, detail="User was not found")
