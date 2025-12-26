"""
Advanced Encryption Service
Implements field-level encryption, end-to-end encryption, and key management
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
import os
import secrets
from typing import Dict, Any, Optional
import json


class AdvancedEncryptionService:
    """Advanced encryption service with multiple encryption methods"""
    
    def __init__(self, master_key: Optional[bytes] = None):
        """
        Initialize encryption service
        
        Args:
            master_key: Master encryption key (32 bytes). If None, generates new key.
        """
        if master_key is None:
            master_key = Fernet.generate_key()
        
        self.master_key = master_key
        self.fernet = Fernet(master_key)
    
    def encrypt_field(self, data: str) -> str:
        """
        Encrypt a single field using Fernet (symmetric encryption)
        
        Args:
            data: Data to encrypt
        
        Returns:
            Base64 encoded encrypted data
        """
        if not data:
            return data
        
        encrypted = self.fernet.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt_field(self, encrypted_data: str) -> str:
        """
        Decrypt a single field
        
        Args:
            encrypted_data: Encrypted data
        
        Returns:
            Decrypted string
        """
        if not encrypted_data:
            return encrypted_data
        
        decrypted = self.fernet.decrypt(encrypted_data.encode())
        return decrypted.decode()
    
    def encrypt_json(self, data: Dict[str, Any]) -> str:
        """
        Encrypt JSON data
        
        Args:
            data: Dictionary to encrypt
        
        Returns:
            Encrypted JSON string
        """
        json_str = json.dumps(data)
        return self.encrypt_field(json_str)
    
    def decrypt_json(self, encrypted_data: str) -> Dict[str, Any]:
        """
        Decrypt JSON data
        
        Args:
            encrypted_data: Encrypted JSON string
        
        Returns:
            Decrypted dictionary
        """
        json_str = self.decrypt_field(encrypted_data)
        return json.loads(json_str)
    
    def encrypt_with_aes_256(self, data: bytes, key: bytes) -> Dict[str, str]:
        """
        Encrypt data using AES-256-GCM for authenticated encryption
        
        Args:
            data: Data to encrypt
            key: 32-byte encryption key
        
        Returns:
            Dictionary with encrypted data, nonce, and tag
        """
        # Generate random nonce
        nonce = os.urandom(12)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce),
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "tag": base64.b64encode(encryptor.tag).decode()
        }
    
    def decrypt_with_aes_256(
        self, 
        ciphertext: str, 
        key: bytes, 
        nonce: str, 
        tag: str
    ) -> bytes:
        """
        Decrypt AES-256-GCM encrypted data
        
        Args:
            ciphertext: Base64 encoded ciphertext
            key: 32-byte encryption key
            nonce: Base64 encoded nonce
            tag: Base64 encoded authentication tag
        
        Returns:
            Decrypted data
        """
        # Decode from base64
        ciphertext_bytes = base64.b64decode(ciphertext)
        nonce_bytes = base64.b64decode(nonce)
        tag_bytes = base64.b64decode(tag)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce_bytes, tag_bytes),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        
        return plaintext
    
    def generate_key_from_password(
        self, 
        password: str, 
        salt: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt for key derivation (generated if None)
        
        Returns:
            Dictionary with key and salt
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode())
        
        return {
            "key": key,
            "salt": base64.b64encode(salt).decode()
        }
    
    def generate_rsa_keypair(self, key_size: int = 2048) -> Dict[str, str]:
        """
        Generate RSA key pair for asymmetric encryption
        
        Args:
            key_size: Key size in bits (2048 or 4096)
        
        Returns:
            Dictionary with private and public keys (PEM format)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        # Serialize keys to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        return {
            "private_key": private_pem,
            "public_key": public_pem
        }
    
    def encrypt_with_public_key(self, data: bytes, public_key_pem: str) -> str:
        """
        Encrypt data with RSA public key
        
        Args:
            data: Data to encrypt
            public_key_pem: Public key in PEM format
        
        Returns:
            Base64 encoded encrypted data
        """
        # Load public key
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(),
            backend=default_backend()
        )
        
        # Encrypt
        encrypted = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return base64.b64encode(encrypted).decode()
    
    def decrypt_with_private_key(
        self, 
        encrypted_data: str, 
        private_key_pem: str
    ) -> bytes:
        """
        Decrypt data with RSA private key
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            private_key_pem: Private key in PEM format
        
        Returns:
            Decrypted data
        """
        # Load private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )
        
        # Decrypt
        encrypted_bytes = base64.b64decode(encrypted_data)
        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return decrypted


class DataAnonymizer:
    """Anonymize and pseudonymize sensitive data for GDPR compliance"""
    
    @staticmethod
    def anonymize_email(email: str) -> str:
        """
        Anonymize email address
        
        Args:
            email: Email to anonymize
        
        Returns:
            Anonymized email
        """
        if '@' not in email:
            return "***@***.***"
        
        local, domain = email.split('@')
        if len(local) <= 2:
            anonymized_local = local[0] + '*'
        else:
            anonymized_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            anonymized_domain = domain_parts[0][0] + '***.' + domain_parts[-1]
        else:
            anonymized_domain = '***'
        
        return f"{anonymized_local}@{anonymized_domain}"
    
    @staticmethod
    def anonymize_phone(phone: str) -> str:
        """
        Anonymize phone number
        
        Args:
            phone: Phone number to anonymize
        
        Returns:
            Anonymized phone
        """
        # Keep only last 4 digits
        if len(phone) > 4:
            return '*' * (len(phone) - 4) + phone[-4:]
        return '***'
    
    @staticmethod
    def anonymize_ip(ip_address: str) -> str:
        """
        Anonymize IP address (keep network, mask host)
        
        Args:
            ip_address: IP to anonymize
        
        Returns:
            Anonymized IP
        """
        parts = ip_address.split('.')
        if len(parts) == 4:
            # Keep first two octets for IPv4
            return f"{parts[0]}.{parts[1]}.***. ***"
        
        # IPv6 - keep first 4 groups
        parts = ip_address.split(':')
        if len(parts) >= 4:
            return ':'.join(parts[:4]) + ':****:****:****:****'
        
        return '***'
    
    @staticmethod
    def generate_pseudonym(original_id: str, salt: str) -> str:
        """
        Generate consistent pseudonym from ID
        
        Args:
            original_id: Original identifier
            salt: Salt for hashing
        
        Returns:
            Pseudonymized ID
        """
        import hashlib
        
        combined = f"{original_id}{salt}"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        # Return first 16 characters for readability
        return f"user_{hashed[:16]}"
    
    @staticmethod
    def mask_sensitive_data(text: str, patterns: Dict[str, str]) -> str:
        """
        Mask sensitive patterns in text
        
        Args:
            text: Text to mask
            patterns: Dictionary of regex patterns and replacements
        
        Returns:
            Masked text
        """
        import re
        
        masked = text
        
        # Default patterns
        default_patterns = {
            r'\b\d{3}-\d{2}-\d{4}\b': '***-**-****',  # SSN
            r'\b\d{16}\b': '****-****-****-****',      # Credit card
            r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b': '***@***.***'  # Email
        }
        
        all_patterns = {**default_patterns, **patterns}
        
        for pattern, replacement in all_patterns.items():
            masked = re.sub(pattern, replacement, masked, flags=re.IGNORECASE)
        
        return masked
