"""
SphereRyder Security Services - Secure Password Manager
Core Module with AES-256-GCM Encryption

This module provides the core functionality for secure password management including:
- AES-256-GCM encryption for password storage
- PBKDF2 key derivation from master passwords
- Bcrypt hashing for user authentication
- Secure password generation
- CRUD operations for password entries
- Activity logging
"""

import os
import json
import secrets
import string
import hashlib
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt


class PasswordManager:
    """
    Main Password Manager class that handles all password operations
    with military-grade AES-256-GCM encryption
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the Password Manager
        
        Args:
            data_dir: Directory to store all password manager data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths for different data stores
        self.users_file = self.data_dir / "users.json"
        self.passwords_file = self.data_dir / "passwords.json"
        self.logs_file = self.data_dir / "activity.log"
        
        # Initialize data structures
        self._initialize_data_files()
        
        # Current logged-in user
        self.current_user: Optional[str] = None
        self.current_key: Optional[bytes] = None
    
    def _initialize_data_files(self):
        """
        Initialize data files with pre-configured test accounts if they don't exist
        
        Pre-configured test accounts:
        - Username: admin, Password: Admin@2024
        - Username: testuser, Password: Test@2024
        - Username: demo, Password: Demo@2024
        """
        # Initialize users file with test accounts
        if not self.users_file.exists():
            test_users = {
                "admin": {
                    "password_hash": self._hash_password("Admin@2024"),
                    "salt": base64.b64encode(os.urandom(32)).decode('utf-8'),
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                },
                "testuser": {
                    "password_hash": self._hash_password("Test@2024"),
                    "salt": base64.b64encode(os.urandom(32)).decode('utf-8'),
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                },
                "demo": {
                    "password_hash": self._hash_password("Demo@2024"),
                    "salt": base64.b64encode(os.urandom(32)).decode('utf-8'),
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                }
            }
            self._write_json(self.users_file, test_users)
            self._log_activity("SYSTEM", "Initialized users database with test accounts")
        
        # Initialize passwords file
        if not self.passwords_file.exists():
            # Structure: {username: {domain: {encrypted_data, nonce, timestamp}}}
            self._write_json(self.passwords_file, {})
            self._log_activity("SYSTEM", "Initialized passwords database")
        
        # Initialize logs file
        if not self.logs_file.exists():
            self.logs_file.touch()
            self._log_activity("SYSTEM", "Password Manager initialized")
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt for secure storage
        
        Args:
            password: Plain text password
            
        Returns:
            Bcrypt hashed password as string
        """
        # Generate salt and hash password with bcrypt (cost factor 12)
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a bcrypt hash
        
        Args:
            password: Plain text password to verify
            hashed: Stored bcrypt hash
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive a 256-bit encryption key from password using PBKDF2
        
        Args:
            password: Master password
            salt: Unique salt for the user
            
        Returns:
            32-byte (256-bit) encryption key
        """
        # Use PBKDF2 with SHA-256, 480,000 iterations (OWASP 2023 recommendation)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=480000,
        )
        return kdf.derive(password.encode('utf-8'))
    
    def _encrypt_password(self, password: str, key: bytes) -> Tuple[str, str]:
        """
        Encrypt a password using AES-256-GCM
        
        Args:
            password: Plain text password to encrypt
            key: 256-bit encryption key
            
        Returns:
            Tuple of (encrypted_data, nonce) both base64 encoded
        """
        # Generate random 96-bit nonce for GCM mode
        nonce = os.urandom(12)
        
        # Create AES-GCM cipher
        aesgcm = AESGCM(key)
        
        # Encrypt the password (GCM provides authentication)
        encrypted = aesgcm.encrypt(nonce, password.encode('utf-8'), None)
        
        # Return base64 encoded values for JSON storage
        return (
            base64.b64encode(encrypted).decode('utf-8'),
            base64.b64encode(nonce).decode('utf-8')
        )
    
    def _decrypt_password(self, encrypted_data: str, nonce: str, key: bytes) -> str:
        """
        Decrypt a password using AES-256-GCM
        
        Args:
            encrypted_data: Base64 encoded encrypted password
            nonce: Base64 encoded nonce
            key: 256-bit encryption key
            
        Returns:
            Decrypted plain text password
        """
        # Decode from base64
        encrypted_bytes = base64.b64decode(encrypted_data)
        nonce_bytes = base64.b64decode(nonce)
        
        # Create AES-GCM cipher
        aesgcm = AESGCM(key)
        
        # Decrypt and verify
        decrypted = aesgcm.decrypt(nonce_bytes, encrypted_bytes, None)
        
        return decrypted.decode('utf-8')
    
    def _read_json(self, filepath: Path) -> Dict:
        """
        Safely read JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Dictionary from JSON file
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_json(self, filepath: Path, data: Dict):
        """
        Safely write to JSON file
        
        Args:
            filepath: Path to JSON file
            data: Dictionary to write
        """
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log_activity(self, username: str, action: str):
        """
        Log user activity with timestamp
        
        Args:
            username: Username performing the action
            action: Description of the action
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {username}: {action}\n"
        
        with open(self.logs_file, 'a') as f:
            f.write(log_entry)
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user with username and password
        
        Args:
            username: Username to authenticate
            password: Master password
            
        Returns:
            True if authentication successful, False otherwise
        """
        users = self._read_json(self.users_file)
        
        # Check if user exists
        if username not in users:
            self._log_activity(username, "Failed login attempt - user not found")
            return False
        
        user_data = users[username]
        
        # Verify password
        if not self._verify_password(password, user_data['password_hash']):
            self._log_activity(username, "Failed login attempt - incorrect password")
            return False
        
        # Authentication successful
        self.current_user = username
        
        # Derive encryption key from master password
        salt = base64.b64decode(user_data['salt'])
        self.current_key = self._derive_key(password, salt)
        
        # Update last login
        users[username]['last_login'] = datetime.now().isoformat()
        self._write_json(self.users_file, users)
        
        self._log_activity(username, "Successful login")
        return True
    
    def change_master_password(self, old_password: str, new_password: str) -> bool:
        """
        Change the master password for the current user
        Re-encrypts all passwords with new key
        
        Args:
            old_password: Current master password
            new_password: New master password
            
        Returns:
            True if password changed successfully, False otherwise
        """
        if not self.current_user:
            return False
        
        users = self._read_json(self.users_file)
        user_data = users[self.current_user]
        
        # Verify old password
        if not self._verify_password(old_password, user_data['password_hash']):
            self._log_activity(self.current_user, "Failed password change - incorrect old password")
            return False
        
        # Get all passwords for this user and decrypt with old key
        passwords = self._read_json(self.passwords_file)
        user_passwords = passwords.get(self.current_user, {})
        
        decrypted_passwords = {}
        for domain, pwd_data in user_passwords.items():
            decrypted_passwords[domain] = self._decrypt_password(
                pwd_data['encrypted_data'],
                pwd_data['nonce'],
                self.current_key
            )
        
        # Generate new salt and hash new password
        new_salt = os.urandom(32)
        new_hash = self._hash_password(new_password)
        
        # Derive new encryption key
        new_key = self._derive_key(new_password, new_salt)
        
        # Re-encrypt all passwords with new key
        re_encrypted = {}
        for domain, plain_password in decrypted_passwords.items():
            encrypted_data, nonce = self._encrypt_password(plain_password, new_key)
            re_encrypted[domain] = {
                'encrypted_data': encrypted_data,
                'nonce': nonce,
                'updated_at': datetime.now().isoformat()
            }
        
        # Update user data
        users[self.current_user]['password_hash'] = new_hash
        users[self.current_user]['salt'] = base64.b64encode(new_salt).decode('utf-8')
        self._write_json(self.users_file, users)
        
        # Update passwords
        passwords[self.current_user] = re_encrypted
        self._write_json(self.passwords_file, passwords)
        
        # Update current key
        self.current_key = new_key
        
        self._log_activity(self.current_user, "Master password changed successfully")
        return True
    
    def generate_password(self, length: int = 16, 
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_special: bool = True) -> str:
        """
        Generate a cryptographically secure random password
        
        Args:
            length: Length of password (minimum 12)
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include digits
            use_special: Include special characters
            
        Returns:
            Generated secure password
        """
        if length < 12:
            length = 12  # Enforce minimum length
        
        # Build character set
        chars = ""
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            # Default to all character types if none selected
            chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        
        # Generate password ensuring at least one character from each selected type
        password = []
        
        if use_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
        if use_digits:
            password.append(secrets.choice(string.digits))
        if use_special:
            password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill remaining length with random characters
        remaining = length - len(password)
        password.extend(secrets.choice(chars) for _ in range(remaining))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def add_password(self, domain: str, password: Optional[str] = None, 
                    username: Optional[str] = None, notes: Optional[str] = None) -> bool:
        """
        Add a new password entry for a domain
        
        Args:
            domain: Domain/service name (e.g., 'gmail.com', 'github')
            password: Password to store (auto-generated if None)
            username: Optional username for the service
            notes: Optional notes
            
        Returns:
            True if added successfully, False otherwise
        """
        if not self.current_user or not self.current_key:
            return False
        
        # Auto-generate password if not provided
        if password is None:
            password = self.generate_password(16)
        
        # Encrypt the password
        encrypted_data, nonce = self._encrypt_password(password, self.current_key)
        
        # Read current passwords
        passwords = self._read_json(self.passwords_file)
        
        # Initialize user's password dict if not exists
        if self.current_user not in passwords:
            passwords[self.current_user] = {}
        
        # Store encrypted password with metadata
        passwords[self.current_user][domain] = {
            'encrypted_data': encrypted_data,
            'nonce': nonce,
            'username': username,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Write to file
        self._write_json(self.passwords_file, passwords)
        
        self._log_activity(self.current_user, f"Added password for domain: {domain}")
        return True
    
    def get_password(self, domain: str) -> Optional[Dict]:
        """
        Retrieve and decrypt a password for a domain
        
        Args:
            domain: Domain/service name
            
        Returns:
            Dictionary with password and metadata, or None if not found
        """
        if not self.current_user or not self.current_key:
            return None
        
        passwords = self._read_json(self.passwords_file)
        
        if self.current_user not in passwords:
            return None
        
        if domain not in passwords[self.current_user]:
            return None
        
        pwd_data = passwords[self.current_user][domain]
        
        # Decrypt password
        try:
            decrypted_password = self._decrypt_password(
                pwd_data['encrypted_data'],
                pwd_data['nonce'],
                self.current_key
            )
            
            self._log_activity(self.current_user, f"Retrieved password for domain: {domain}")
            
            return {
                'password': decrypted_password,
                'username': pwd_data.get('username'),
                'notes': pwd_data.get('notes'),
                'created_at': pwd_data.get('created_at'),
                'updated_at': pwd_data.get('updated_at')
            }
        except Exception as e:
            self._log_activity(self.current_user, f"Failed to decrypt password for {domain}: {str(e)}")
            return None
    
    def get_all_domains(self) -> List[str]:
        """
        Get list of all domains for current user
        
        Returns:
            List of domain names
        """
        if not self.current_user:
            return []
        
        passwords = self._read_json(self.passwords_file)
        
        if self.current_user not in passwords:
            return []
        
        return list(passwords[self.current_user].keys())
    
    def update_password(self, domain: str, new_password: Optional[str] = None) -> bool:
        """
        Update password for an existing domain
        
        Args:
            domain: Domain/service name
            new_password: New password (auto-generated if None)
            
        Returns:
            True if updated successfully, False otherwise
        """
        if not self.current_user or not self.current_key:
            return False
        
        passwords = self._read_json(self.passwords_file)
        
        if self.current_user not in passwords or domain not in passwords[self.current_user]:
            return False
        
        # Auto-generate if not provided
        if new_password is None:
            new_password = self.generate_password(16)
        
        # Encrypt new password
        encrypted_data, nonce = self._encrypt_password(new_password, self.current_key)
        
        # Update only password and timestamp, keep other metadata
        passwords[self.current_user][domain]['encrypted_data'] = encrypted_data
        passwords[self.current_user][domain]['nonce'] = nonce
        passwords[self.current_user][domain]['updated_at'] = datetime.now().isoformat()
        
        self._write_json(self.passwords_file, passwords)
        
        self._log_activity(self.current_user, f"Updated password for domain: {domain}")
        return True
    
    def delete_password(self, domain: str) -> bool:
        """
        Delete a password entry
        
        Args:
            domain: Domain/service name
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.current_user:
            return False
        
        passwords = self._read_json(self.passwords_file)
        
        if self.current_user not in passwords or domain not in passwords[self.current_user]:
            return False
        
        # Delete the entry
        del passwords[self.current_user][domain]
        
        self._write_json(self.passwords_file, passwords)
        
        self._log_activity(self.current_user, f"Deleted password for domain: {domain}")
        return True
    
    def get_activity_logs(self, limit: int = 50) -> List[str]:
        """
        Get recent activity logs
        
        Args:
            limit: Maximum number of log entries to return
            
        Returns:
            List of log entries
        """
        if not self.logs_file.exists():
            return []
        
        with open(self.logs_file, 'r') as f:
            logs = f.readlines()
        
        # Return last 'limit' entries
        return logs[-limit:]
    
    def logout(self):
        """
        Logout current user and clear sensitive data from memory
        """
        if self.current_user:
            self._log_activity(self.current_user, "Logged out")
        
        self.current_user = None
        self.current_key = None
