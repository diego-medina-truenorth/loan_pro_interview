from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from ..authentication import authenticate_user, generate_access_token
from ..model.orm import User, Record, Operation
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate an access token and return it in the response
    access_token = generate_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/calculator/{operation_type}")
def calculate(
    operation_type: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has sufficient balance
    if current_user.balance < current_user.operation_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    # Perform the requested calculation based on operation_type and amount
    if operation_type == "addition":
        result = amount + current_user.balance
    elif operation_type == "subtraction":
        result = current_user.balance - amount
    elif operation_type == "multiplication":
        result = amount * current_user.balance
    elif operation_type == "division":
        result = current_user.balance / amount
    elif operation_type == "square_root":
        result = current_user.balance ** 0.5
    elif operation_type == "random_string":
        result = "Random string"

    # Deduct the operation cost from the user's balance
    current_user.balance -= current_user.operation_cost

    # Create a record of the operation
    record = Record(
        operation_id=current_user.operation_id,
        user_id=current_user.id,
        amount=amount,
        user_balance=current_user.balance,
        operation_response=result,
        date=datetime.now()
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"result": result}