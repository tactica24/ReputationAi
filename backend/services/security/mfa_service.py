"""
Multi-Factor Authentication (MFA) Service
Supports TOTP, SMS, and Email-based 2FA
"""

import pyotp
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import hashlib


class MFAService:
    """Multi-Factor Authentication service supporting multiple 2FA methods"""
    
    def __init__(self):
        self.issuer_name = "AI Guardian"
    
    def generate_totp_secret(self, user_email: str) -> Dict[str, str]:
        """
        Generate a new TOTP secret for a user
        
        Returns:
            Dictionary with secret, provisioning URI, and QR code
        """
        # Generate random secret
        secret = pyotp.random_base32()
        
        # Create TOTP object
        totp = pyotp.TOTP(secret)
        
        # Generate provisioning URI for QR code
        provisioning_uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=self.issuer_name
        )
        
        # Generate QR code
        qr_code = self._generate_qr_code(provisioning_uri)
        
        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "qr_code": qr_code,
            "algorithm": "SHA1",
            "digits": 6,
            "period": 30
        }
    
    def verify_totp(self, secret: str, token: str, window: int = 1) -> bool:
        """
        Verify a TOTP token
        
        Args:
            secret: The user's TOTP secret
            token: The token to verify
            window: Number of time windows to check (for clock drift)
        
        Returns:
            True if token is valid
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=window)
    
    def generate_backup_codes(self, count: int = 10) -> list[str]:
        """
        Generate backup codes for account recovery
        
        Args:
            count: Number of backup codes to generate
        
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX for readability
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)
        
        return codes
    
    def hash_backup_code(self, code: str) -> str:
        """
        Hash a backup code for secure storage
        
        Args:
            code: The backup code to hash
        
        Returns:
            Hashed code
        """
        return hashlib.sha256(code.encode()).hexdigest()
    
    def verify_backup_code(self, code: str, hashed_code: str) -> bool:
        """
        Verify a backup code against its hash
        
        Args:
            code: The code to verify
            hashed_code: The stored hash
        
        Returns:
            True if code is valid
        """
        return self.hash_backup_code(code) == hashed_code
    
    def generate_sms_code(self, length: int = 6) -> str:
        """
        Generate a numeric code for SMS verification
        
        Args:
            length: Length of the code
        
        Returns:
            Numeric code as string
        """
        # Generate random number with specified length
        code = ''.join([str(secrets.randbelow(10)) for _ in range(length)])
        return code
    
    def generate_email_code(self, length: int = 6) -> str:
        """
        Generate an alphanumeric code for email verification
        
        Args:
            length: Length of the code
        
        Returns:
            Alphanumeric code
        """
        # Generate alphanumeric code
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        return code
    
    def _generate_qr_code(self, data: str) -> str:
        """
        Generate a QR code and return as base64 encoded image
        
        Args:
            data: Data to encode in QR code
        
        Returns:
            Base64 encoded PNG image
        """
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    def create_session_token(self, user_id: int, expires_in: int = 300) -> Dict[str, Any]:
        """
        Create a temporary session token for MFA verification
        
        Args:
            user_id: User ID
            expires_in: Token expiration in seconds (default 5 minutes)
        
        Returns:
            Session token and expiration
        """
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        return {
            "token": token,
            "user_id": user_id,
            "expires_at": expires_at,
            "verified": False
        }
    
    def validate_device_fingerprint(
        self, 
        user_agent: str, 
        ip_address: str,
        stored_fingerprint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create and validate device fingerprint for trusted device functionality
        
        Args:
            user_agent: User's browser user agent
            ip_address: User's IP address
            stored_fingerprint: Previously stored fingerprint (if any)
        
        Returns:
            Fingerprint info and validation result
        """
        # Create fingerprint from device characteristics
        fingerprint_data = f"{user_agent}|{ip_address}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        
        is_trusted = stored_fingerprint == fingerprint if stored_fingerprint else False
        
        return {
            "fingerprint": fingerprint,
            "is_trusted": is_trusted,
            "requires_mfa": not is_trusted
        }


class MFAAttemptTracker:
    """Track and limit MFA verification attempts to prevent brute force"""
    
    def __init__(self, max_attempts: int = 5, lockout_duration: int = 900):
        """
        Initialize attempt tracker
        
        Args:
            max_attempts: Maximum failed attempts before lockout
            lockout_duration: Lockout duration in seconds (default 15 min)
        """
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self.attempts = {}  # In production, use Redis
    
    def record_attempt(self, user_id: int, success: bool) -> Dict[str, Any]:
        """
        Record a verification attempt
        
        Args:
            user_id: User ID
            success: Whether the attempt was successful
        
        Returns:
            Attempt status
        """
        if user_id not in self.attempts:
            self.attempts[user_id] = {
                "count": 0,
                "locked_until": None,
                "last_attempt": None
            }
        
        user_attempts = self.attempts[user_id]
        
        # Check if currently locked out
        if user_attempts["locked_until"]:
            if datetime.utcnow() < user_attempts["locked_until"]:
                return {
                    "allowed": False,
                    "locked": True,
                    "locked_until": user_attempts["locked_until"],
                    "remaining_attempts": 0
                }
            else:
                # Lockout expired, reset
                user_attempts["count"] = 0
                user_attempts["locked_until"] = None
        
        if success:
            # Reset on success
            user_attempts["count"] = 0
            user_attempts["locked_until"] = None
        else:
            # Increment failed attempts
            user_attempts["count"] += 1
            user_attempts["last_attempt"] = datetime.utcnow()
            
            # Lock if max attempts reached
            if user_attempts["count"] >= self.max_attempts:
                user_attempts["locked_until"] = (
                    datetime.utcnow() + timedelta(seconds=self.lockout_duration)
                )
                return {
                    "allowed": False,
                    "locked": True,
                    "locked_until": user_attempts["locked_until"],
                    "remaining_attempts": 0
                }
        
        remaining = self.max_attempts - user_attempts["count"]
        
        return {
            "allowed": True,
            "locked": False,
            "remaining_attempts": remaining,
            "attempts_used": user_attempts["count"]
        }
    
    def is_locked_out(self, user_id: int) -> bool:
        """Check if a user is currently locked out"""
        if user_id not in self.attempts:
            return False
        
        user_attempts = self.attempts[user_id]
        if user_attempts["locked_until"]:
            return datetime.utcnow() < user_attempts["locked_until"]
        
        return False
    
    def reset_attempts(self, user_id: int):
        """Reset attempts for a user (e.g., after successful login)"""
        if user_id in self.attempts:
            del self.attempts[user_id]
