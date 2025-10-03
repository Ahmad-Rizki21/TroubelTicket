# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, security
from datetime import datetime, timedelta
import secrets

# ==================================
# Fungsi CRUD untuk User (Diperbarui)
# ==================================
from sqlalchemy.orm import joinedload

# ==================================
# Ticket Code Generation
# ==================================
def generate_sequential_ticket_code(db: Session) -> str:
    """
    Generate sequential ticket code in format AG-00000001, AG-00000002, etc.
    """
    # Get the highest ticket code from existing tickets
    last_ticket = db.query(models.Ticket).filter(
        models.Ticket.ticket_code.like('AG-%')
    ).order_by(models.Ticket.id.desc()).first()

    if last_ticket and last_ticket.ticket_code:
        # Extract the number from the last ticket code
        try:
            last_number = int(last_ticket.ticket_code.split('-')[1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            # If there's an issue with parsing, start from 1
            next_number = 1
    else:
        # No existing tickets with AG- prefix, start from 1
        next_number = 1

    # Format the ticket code with leading zeros
    return f"AG-{next_number:08d}"

def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.role).joinedload(models.Role.permissions)).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).options(joinedload(models.User.role).joinedload(models.Role.permissions)).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload(models.User.role).joinedload(models.Role.permissions)).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # Gunakan fungsi hashing dari security.py
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,  # Simpan hash, bukan password asli
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Return the user with properly loaded relationships
    return get_user(db, db_user.id)

def update_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    """
    Memperbarui password pengguna.
    """
    hashed_password = security.get_password_hash(new_password)
    user.password_hash = hashed_password
    db.add(user)
    db.commit()
    # Refresh the user to get the latest data with relationships
    db.refresh(user)
    # Return the user with properly loaded relationships
    return get_user(db, user.id)

def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> models.User | None:
    db_user = get_user(db, user_id=user_id)  # Using the updated function that loads relationships
    if not db_user:
        return None
    
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password": # Handle password hashing if password is being updated
            if value:
                db_user.password_hash = security.get_password_hash(value)
        else:
            setattr(db_user, key, value)
            
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Return the user with properly loaded relationships
    return get_user(db, user_id)

def delete_user(db: Session, user_id: int) -> models.User | None:
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None

    # Unassign tickets associated with this user before deletion
    db.query(models.Ticket).filter(models.Ticket.assignee_id == user_id).update({"assignee_id": None})

    db.delete(db_user)
    db.commit()
    return db_user

# ==================================
# Fungsi CRUD untuk Role
# ==================================
def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_in: schemas.RoleUpdate) -> models.Role | None:
    db_role = get_role(db, role_id=role_id)
    if not db_role:
        return None
    
    update_data = role_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
            
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int, force: bool = False) -> models.Role | None:
    db_role = get_role(db, role_id=role_id)
    if not db_role:
        return None
    
    # Cek apakah role sedang digunakan oleh user
    users_with_role = db.query(models.User).filter(models.User.role_id == role_id).all()
    
    if users_with_role:
        if force:
            # Jika force=True, pindahkan semua user ke role default (misalnya role dengan id=1 atau role 'user')
            # Cari role 'user' sebagai fallback
            default_role = db.query(models.Role).filter(models.Role.name == 'user').first()
            if not default_role:
                # Jika tidak ada role 'user', gunakan role dengan id terkecil (selain yang akan dihapus)
                default_role = db.query(models.Role).filter(models.Role.id != role_id).order_by(models.Role.id).first()
            
            if default_role:
                # Update semua user untuk menggunakan role default
                for user in users_with_role:
                    user.role_id = default_role.id
                db.commit()
            else:
                raise ValueError(f"Tidak bisa menghapus role '{db_role.name}' karena tidak ditemukan role alternatif dan masih digunakan oleh {len(users_with_role)} user(s)")
        else:
            # Jika force=False (default), lempar error
            raise ValueError(f"Role '{db_role.name}' tidak bisa dihapus karena masih digunakan oleh {len(users_with_role)} user(s)")

    # Lakukan penghapusan
    db.delete(db_role)
    db.commit()
    return db_role

# ==================================
# Fungsi CRUD untuk Permission
# ==================================
def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str):
    return db.query(models.Permission).filter(models.Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: int, permission_in: schemas.PermissionUpdate) -> models.Permission | None:
    db_permission = get_permission(db, permission_id=permission_id)
    if not db_permission:
        return None
    
    update_data = permission_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permission, key, value)
            
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int) -> models.Permission | None:
    db_permission = get_permission(db, permission_id=permission_id)
    if not db_permission:
        return None
    db.delete(db_permission)
    db.commit()
    return db_permission

def add_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission:
        # Cek apakah permission sudah terkait dengan role
        if permission not in role.permissions:
            role.permissions.append(permission)
            db.commit()
        return role
    return None

def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission:
        try:
            role.permissions.remove(permission)
            db.commit()
            return role
        except ValueError:
            return None # Permission was not in role
    return None


# ==================================
# Fungsi CRUD untuk Ticket
# ==================================
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    # Generate sequential ticket code
    ticket_code = generate_sequential_ticket_code(db)

    db_ticket = models.Ticket(
        ticket_code=ticket_code,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
        reporter_name=ticket.reporter_name,
        reporter_contact=ticket.reporter_contact
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket(db: Session, ticket_id: int, ticket: schemas.TicketUpdate):
    db_ticket = get_ticket(db, ticket_id=ticket_id)
    if not db_ticket:
        return None
    
    update_data = ticket.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
        
    # If status is being changed to 'Closed' and closed_at is not set, set it to current time
    if (hasattr(ticket, 'status') and ticket.status == 'Closed' and 
        (not db_ticket.closed_at or 
         (db_ticket.status != 'Closed' and ticket.status == 'Closed'))):
        from datetime import datetime
        db_ticket.closed_at = datetime.utcnow()
        
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = get_ticket(db, ticket_id=ticket_id)
    if not db_ticket:
        return None
    db.delete(db_ticket)
    db.commit()
    return db_ticket

# ==================================
# Fungsi CRUD untuk TicketAction
# ==================================
def get_actions_for_ticket(db: Session, ticket_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TicketAction).filter(models.TicketAction.ticket_id == ticket_id).offset(skip).limit(limit).all()

def create_ticket_action(db: Session, action: schemas.TicketActionCreate, ticket_id: int, user_id: int):
    # Ambil role_id dari user yang sedang login
    user = get_user(db, user_id)
    if not user:
        return None # Atau raise exception

    db_action = models.TicketAction(
        **action.model_dump(),
        ticket_id=ticket_id,
        user_id=user_id,
        role_id=user.role_id
    )
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

def get_ticket_action(db: Session, action_id: int):
    """Helper function to get a single ticket action by its ID."""
    return db.query(models.TicketAction).filter(models.TicketAction.id == action_id).first()

def update_ticket_action(db: Session, action_id: int, action_in: schemas.TicketActionUpdate) -> models.TicketAction | None:
    """Updates a ticket action."""
    db_action = get_ticket_action(db, action_id=action_id)
    if not db_action:
        return None
    
    update_data = action_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_action, key, value)
            
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


# ==================================
# Fungsi CRUD untuk Remote
# ==================================
def get_remote(db: Session, remote_id: int):
    return db.query(models.Remote).filter(models.Remote.id == remote_id).first()

def get_remotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Remote).offset(skip).limit(limit).all()

def create_remote(db: Session, remote: schemas.RemoteCreate) -> models.Remote:
    db_remote = models.Remote(**remote.model_dump())
    db.add(db_remote)
    db.commit()
    db.refresh(db_remote)
    return db_remote

def update_remote(db: Session, remote_id: int, remote_in: schemas.RemoteUpdate) -> models.Remote | None:
    db_remote = get_remote(db, remote_id=remote_id)
    if not db_remote:
        return None
    
    update_data = remote_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_remote, key, value)
            
    db.add(db_remote)
    db.commit()
    db.refresh(db_remote)
    return db_remote

def delete_remote(db: Session, remote_id: int) -> models.Remote | None:
    db_remote = get_remote(db, remote_id=remote_id)
    if not db_remote:
        return None
    db.delete(db_remote)
    db.commit()
    return db_remote

def create_password_reset_token(db: Session, user: models.User) -> models.PasswordResetToken:
    """
    Membuat dan menyimpan token reset password baru untuk pengguna.
    """
    # Hapus token lama jika ada
    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.user_id == user.id).delete()
    
    token = secrets.token_urlsafe(32)
    # Important: Use timezone-aware datetime objects if your database/app uses them
    expires_at = datetime.now() + timedelta(hours=1)
    
    db_token = models.PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_password_reset_token_by_token(db: Session, token: str) -> models.PasswordResetToken | None:
    """
    Mengambil record token reset password berdasarkan token string.
    """
    return db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()

def delete_password_reset_token(db: Session, token_id: int):
    """
    Menghapus token reset password dari database.
    """
    db_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.id == token_id).first()
    if db_token:
        db.delete(db_token)
        db.commit()
    return db_token