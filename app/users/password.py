"""
Password utilities for user authentication
"""
import secrets
import hashlib
from typing import Optional

# TODO: Install passlib and uncomment for production
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using SHA256 with salt (temporary implementation)"""
    # TODO: Replace with bcrypt when passlib is installed
    salt = "buildbuzz_salt_2024_secure"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # TODO: Replace with bcrypt verification when passlib is installed
    return hash_password(plain_password) == hashed_password

def generate_password(length: int = 12) -> str:
    """Generate a secure random password"""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def generate_temporary_password() -> str:
    """Generate a temporary password for new users"""
    return generate_password(8)

def is_strong_password(password: str) -> tuple[bool, list[str]]:
    """
    Check if password meets strength requirements
    Returns (is_strong, list_of_issues)
    """
    issues = []
    
    if len(password) < 8:
        issues.append("Password must be at least 8 characters long")
    
    if not any(c.islower() for c in password):
        issues.append("Password must contain at least one lowercase letter")
    
    if not any(c.isupper() for c in password):
        issues.append("Password must contain at least one uppercase letter")
    
    if not any(c.isdigit() for c in password):
        issues.append("Password must contain at least one number")
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        issues.append("Password must contain at least one special character")
    
    return len(issues) == 0, issues