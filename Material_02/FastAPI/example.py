from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserSignUp(BaseModel):
    username: str
    name: EmailStr
    password: str

class Settings(BaseModel):
    app_name: str = 'FastAPI App'
    admin_email: str = 'admin@app.com'

def get_settings():
    return Settings


@app.post('/signup')
def signup(user: UserSignUp):
    return {'message': f'{user.username} Logged in successfully!'}

@app.get('/settings')
def get_settings_endpoint(settings: Settings = Depends(get_settings)):
    return settings