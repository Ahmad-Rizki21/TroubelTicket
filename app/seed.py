# seed.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Role, User, Permission # Import Permission
from app.crud import (
    create_user, get_user_by_username, get_role_by_name, 
    get_permission_by_name, create_permission # Import Permission CRUD
)
from app.schemas import UserCreate, PermissionCreate # Import schemas

db = SessionLocal()

# --- Seeding Roles ---
def seed_roles():
    print("Mulai proses seeding data roles...")
    initial_roles = ["admin", "teknisi"]
    for role_name in initial_roles:
        role_exists = get_role_by_name(db, name=role_name)
        if not role_exists:
            new_role = Role(name=role_name)
            db.add(new_role)
            print(f"Role '{role_name}' berhasil dibuat.")
        else:
            print(f"Role '{role_name}' sudah ada.")
    db.commit()
    print("Seeding data roles selesai.")

# --- Seeding Permissions ---
def seed_permissions():
    print("\nMulai proses seeding data permissions...")
    permission_list = [
        # Ticket permissions
        "ticket:create", "ticket:read", "ticket:update", "ticket:delete", "ticket:assign",
        # User permissions
        "user:create", "user:read", "user:update", "user:delete",
        # Permission permissions (permision untuk mengelola permission)
        "permission:create", "permission:read", "permission:update", "permission:delete",
        # Role & Permission management
        "role:create", "role:read", "role:update", "role:delete", "permission:assign"
    ]
    for perm_name in permission_list:
        perm_exists = get_permission_by_name(db, name=perm_name)
        if not perm_exists:
            new_perm_schema = PermissionCreate(name=perm_name)
            create_permission(db, permission=new_perm_schema)
            print(f"Permission '{perm_name}' berhasil dibuat.")
        else:
            print(f"Permission '{perm_name}' sudah ada.")
    db.commit()
    print("Seeding data permissions selesai.")

# --- Seeding Admin User ---
def seed_admin():
    print("\nMulai proses seeding admin user...")
    admin_user = get_user_by_username(db, username="admin")
    if not admin_user:
        admin_role = get_role_by_name(db, name="admin")
        if not admin_role:
            print("Error: Role 'admin' tidak ditemukan. Pastikan role sudah di-seed.")
            return

        admin_user_schema = UserCreate(
            username="admin",
            password="admin", # Default password, harus diganti di production
            role_id=admin_role.id
        )
        create_user(db, user=admin_user_schema)
        print("User 'admin' dengan password 'admin' berhasil dibuat.")
    else:
        print("User 'admin' sudah ada.")

def assign_permissions_to_roles():
    print("\nMenetapkan izin ke peran...")
    
    # Define permissions for each role
    role_permissions = {
        "admin": [
            # All ticket permissions
            "ticket:create", "ticket:read", "ticket:update", "ticket:delete", "ticket:assign",
            # All user permissions
            "user:create", "user:read", "user:update", "user:delete",
            # All permission permissions
            "permission:create", "permission:read", "permission:update", "permission:delete",
            # All role & permission management
            "role:create", "role:read", "role:update", "role:delete", "permission:assign"
        ],
        "teknisi": [
            "ticket:read", "ticket:update", "ticket:assign"
        ]
    }

    for role_name, perm_names in role_permissions.items():
        role = get_role_by_name(db, name=role_name)
        if not role:
            print(f"Peringatan: Peran '{role_name}' tidak ditemukan. Melewati penetapan izin.")
            continue

        # Clear existing permissions to avoid duplicates on re-run
        role.permissions.clear()
        
        for perm_name in perm_names:
            permission = get_permission_by_name(db, name=perm_name)
            if permission:
                role.permissions.append(permission)
                print(f"Izin '{perm_name}' ditambahkan ke peran '{role_name}'.")
            else:
                print(f"Peringatan: Izin '{perm_name}' tidak ditemukan.")
    
    db.commit()
    print("Penetapan izin ke peran selesai.")

if __name__ == "__main__":
    try:
        seed_roles()
        seed_permissions() # Jalankan seeder permission
        assign_permissions_to_roles() # Menetapkan izin ke peran
        seed_admin()
    except Exception as e:
        print(f"Terjadi error saat seeding: {e}")
        db.rollback()
    finally:
        db.close()