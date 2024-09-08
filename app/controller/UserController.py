from fastapi import APIRouter
from app.main import *
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import  User, SessionLocal ,Item
from app.utilize import hash_password, verify_password, create_access_token, get_db, get_current_user
from app.models.models import ItemResponse , ItemCreate , UserCreate ,UserLogin , Token , TokenData 


router = APIRouter()



@router.post("/create_item/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR CREATING ITEM: {str(e)}"
        )
    
     
@router.post("/register/", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    access_token = create_access_token(data={"sub": user.username})
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, token=access_token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"access_token": access_token, "token_type": "bearer"} 


@router.post("/login/", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    message = "Login Successfull"
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    
    db_user.token = access_token
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer", "message": message}