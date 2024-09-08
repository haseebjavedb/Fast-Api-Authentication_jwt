from fastapi import HTTPException, Depends, FastAPI, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from passlib.context import CryptContext
from app.controller.UserController import router as user_router  
from app.controller.HuggingFaceController import HuggingFaceRouter as HFrouter




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1234"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(user_router)

app.include_router(HFrouter)

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI1MDIxMzg5fQ.YyTN_jkmBe6boSDvU9g0SmCP4DFdqTZzIR5Y-DupgXc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






