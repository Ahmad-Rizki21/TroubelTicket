# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets

from .. import schemas, crud, models, security
from ..core.config import settings
from ..database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(tags=["Authentication"])

# Dependency untuk mendapatkan sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, user_id=int(token_data.id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    # Di masa depan, Anda bisa menambahkan pengecekan is_active di sini
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def has_permission(required_permission: str):
    """
    Dependency factory yang mengembalikan dependency function yang memeriksa
    apakah pengguna saat ini memiliki izin yang diperlukan.
    """
    def permission_checker(current_user: models.User = Depends(get_current_active_user)):
        if not current_user.role or not current_user.role.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions. User has no role or permissions.",
            )
        
        user_permissions = {permission.name for permission in current_user.role.permissions}
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Requires '{required_permission}'.",
            )
        return current_user
    return permission_checker

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"--- DEBUG: Password yang diterima: '{form_data.password}' ---")
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": str(user.id)})
    refresh_token = security.create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, user_id=int(token_data.id))
    if user is None:
        raise credentials_exception
        
    access_token = security.create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": token, # Kembalikan refresh token yang sama
        "token_type": "bearer"
    }

@router.post("/forgot-password", response_model=schemas.PasswordResetResponse)
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Endpoint untuk meminta reset password.
    Membuat token, menyimpannya di DB, dan mengembalikannya ke klien.
    """
    user = crud.get_user_by_username(db, username=request.username)
    if not user:
        # Mencegah user enumeration. 
        # Mengembalikan pesan sukses generik tanpa token.
        return {"message": "Jika username Anda terdaftar, Anda akan menerima token reset."}

    # Buat dan simpan token reset
    reset_token = crud.create_password_reset_token(db, user=user)
    
    # Kembalikan token ke frontend
    return {
        "message": "Token reset password telah dibuat.",
        "token": reset_token.token
    }

@router.post("/reset-password", response_model=schemas.PasswordResetResponse)
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Endpoint untuk melakukan reset password dengan token yang valid.
    """
    if request.new_password != request.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password baru dan konfirmasi password tidak cocok"
        )

    # Cari token di database
    token_record = crud.get_password_reset_token_by_token(db, token=request.token)
    
    # Dapatkan waktu saat ini (sadar zona waktu jika perlu)
    # now = datetime.now(timezone.utc) # Jika Anda menggunakan UTC
    now = datetime.utcnow() # Jika Anda menggunakan UTC naive

    if not token_record or token_record.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token tidak valid atau telah kedaluwarsa"
        )

    # Dapatkan pengguna yang terkait dengan token
    user = crud.get_user(db, user_id=token_record.user_id)
    if not user:
        # Seharusnya tidak terjadi jika integritas DB terjaga
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pengguna tidak ditemukan"
        )

    # Update password pengguna
    crud.update_user_password(db, user=user, new_password=request.new_password)

    # Hapus token yang sudah digunakan
    crud.delete_password_reset_token(db, token_id=token_record.id)

    return {"message": "Password berhasil direset"}


@router.post("/change-password", response_model=schemas.PasswordResetResponse)
async def change_password(request: schemas.ChangePasswordRequest, db: Session = Depends(get_db)):
    """
    Endpoint untuk mengganti password berdasarkan username.
    """
    if not request.username or not request.new_password or not request.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Semua field wajib diisi"
        )

    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password minimal 6 karakter"
        )

    if request.new_password != request.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password baru dan konfirmasi password tidak cocok"
        )

    # Cari user berdasarkan username
    user = crud.get_user_by_username(db, username=request.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forgot password feature is not available. Please contact your system administrator. Please check again Username."
        )

    # Update password pengguna
    crud.update_user_password(db, user=user, new_password=request.new_password)

    return {"message": "Password berhasil diubah"}
