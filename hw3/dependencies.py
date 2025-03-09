from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from models import Person
from auth_router import SECRET_KEY, ALGORITHM, UniversityDataHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    handler = UniversityDataHandler()
    user = handler.session.query(Person).filter(Person.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def check_read_only_access(user: Person = Depends(get_current_user)):
    if user.role == 'read_only':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Read only access granted"
        )
    return user
