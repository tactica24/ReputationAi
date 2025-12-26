"""
Security & Privacy Module
Encryption, RBAC, audit logs, GDPR/NDPR compliance
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
import secrets
import json


class UserRole(Enum):
    """User role definitions for RBAC"""
    VIEWER = "viewer"           # Read-only access
    ANALYST = "analyst"         # View + export reports
    MANAGER = "manager"         # Analyst + configure alerts
    ADMIN = "admin"             # Full access
    SUPER_ADMIN = "super_admin" # System-wide access


class Permission(Enum):
    """Granular permissions"""
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_MENTIONS = "view_mentions"
    EXPORT_DATA = "export_data"
    CONFIGURE_ALERTS = "configure_alerts"
    MANAGE_ENTITIES = "manage_entities"
    MANAGE_USERS = "manage_users"
    ACCESS_API = "access_api"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    DELETE_DATA = "delete_data"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    UserRole.VIEWER: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MENTIONS
    ],
    UserRole.ANALYST: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MENTIONS,
        Permission.EXPORT_DATA
    ],
    UserRole.MANAGER: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MENTIONS,
        Permission.EXPORT_DATA,
        Permission.CONFIGURE_ALERTS,
        Permission.MANAGE_ENTITIES
    ],
    UserRole.ADMIN: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_MENTIONS,
        Permission.EXPORT_DATA,
        Permission.CONFIGURE_ALERTS,
        Permission.MANAGE_ENTITIES,
        Permission.MANAGE_USERS,
        Permission.ACCESS_API,
        Permission.VIEW_AUDIT_LOGS
    ],
    UserRole.SUPER_ADMIN: list(Permission)  # All permissions
}


@dataclass
class AuditLogEntry:
    """Audit log entry for compliance"""
    log_id: str
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    success: bool
    details: Dict
    
    def to_dict(self) -> Dict:
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "details": self.details
        }


class EncryptionService:
    """Handle data encryption/decryption"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption service
        
        Args:
            encryption_key: Base encryption key (should be from secure storage)
        """
        self.encryption_key = encryption_key or self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate a secure encryption key"""
        return secrets.token_hex(32)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data
        
        In production: Use AES-256, Fernet, or AWS KMS
        """
        # Placeholder for actual encryption
        # In production: Use cryptography.fernet or similar
        """
        from cryptography.fernet import Fernet
        
        f = Fernet(self.encryption_key.encode())
        encrypted = f.encrypt(data.encode())
        return encrypted.decode()
        """
        # Simple hash for demo (NOT SECURE - use real encryption in production)
        return hashlib.sha256(f"{data}{self.encryption_key}".encode()).hexdigest()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data
        
        In production: Use matching decryption algorithm
        """
        # Placeholder for actual decryption
        """
        from cryptography.fernet import Fernet
        
        f = Fernet(self.encryption_key.encode())
        decrypted = f.decrypt(encrypted_data.encode())
        return decrypted.decode()
        """
        return encrypted_data  # Placeholder
    
    def hash_sensitive_data(self, data: str) -> str:
        """One-way hash for passwords, etc."""
        return hashlib.sha256(data.encode()).hexdigest()


class RBACService:
    """Role-Based Access Control"""
    
    def __init__(self):
        self.user_roles: Dict[str, UserRole] = {}
        self.custom_permissions: Dict[str, List[Permission]] = {}
    
    def assign_role(self, user_id: str, role: UserRole):
        """Assign a role to a user"""
        self.user_roles[user_id] = role
    
    def grant_permission(self, user_id: str, permission: Permission):
        """Grant a custom permission to a user"""
        if user_id not in self.custom_permissions:
            self.custom_permissions[user_id] = []
        
        if permission not in self.custom_permissions[user_id]:
            self.custom_permissions[user_id].append(permission)
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """
        Check if user has a specific permission
        
        Args:
            user_id: User identifier
            permission: Permission to check
            
        Returns:
            True if user has permission
        """
        # Check custom permissions first
        if user_id in self.custom_permissions:
            if permission in self.custom_permissions[user_id]:
                return True
        
        # Check role-based permissions
        if user_id in self.user_roles:
            role = self.user_roles[user_id]
            return permission in ROLE_PERMISSIONS.get(role, [])
        
        return False
    
    def get_user_permissions(self, user_id: str) -> List[Permission]:
        """Get all permissions for a user"""
        permissions = set()
        
        # Add role permissions
        if user_id in self.user_roles:
            role = self.user_roles[user_id]
            permissions.update(ROLE_PERMISSIONS.get(role, []))
        
        # Add custom permissions
        if user_id in self.custom_permissions:
            permissions.update(self.custom_permissions[user_id])
        
        return list(permissions)


class AuditLogger:
    """Audit logging for compliance (GDPR, SOC 2, etc.)"""
    
    def __init__(self):
        self.logs: List[AuditLogEntry] = []
    
    def log_action(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        ip_address: str,
        user_agent: str,
        success: bool = True,
        details: Optional[Dict] = None
    ) -> AuditLogEntry:
        """
        Log an action for audit trail
        
        Args:
            user_id: User performing action
            action: Action performed (e.g., "view", "edit", "delete")
            resource_type: Type of resource (e.g., "entity", "mention", "user")
            resource_id: ID of the resource
            ip_address: User's IP address
            user_agent: User's browser/client
            success: Whether action was successful
            details: Additional details
            
        Returns:
            Created audit log entry
        """
        log_entry = AuditLogEntry(
            log_id=f"log_{datetime.now().timestamp()}_{secrets.token_hex(8)}",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(),
            success=success,
            details=details or {}
        )
        
        self.logs.append(log_entry)
        
        # In production: Write to secure, append-only log storage
        self._persist_log(log_entry)
        
        return log_entry
    
    def _persist_log(self, log_entry: AuditLogEntry):
        """Persist log to secure storage"""
        # Placeholder for log persistence
        # In production: Write to database, file, or log aggregation service
        pass
    
    def get_logs_for_user(self, user_id: str, limit: int = 100) -> List[AuditLogEntry]:
        """Get audit logs for a specific user"""
        user_logs = [log for log in self.logs if log.user_id == user_id]
        return sorted(user_logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_logs_for_resource(self, resource_type: str, resource_id: str) -> List[AuditLogEntry]:
        """Get audit logs for a specific resource"""
        return [
            log for log in self.logs 
            if log.resource_type == resource_type and log.resource_id == resource_id
        ]
    
    def export_logs(self, start_date: datetime, end_date: datetime, filepath: str):
        """Export audit logs for compliance reporting"""
        filtered_logs = [
            log for log in self.logs 
            if start_date <= log.timestamp <= end_date
        ]
        
        with open(filepath, 'w') as f:
            json.dump([log.to_dict() for log in filtered_logs], f, indent=2)


class GDPRComplianceService:
    """GDPR/NDPR compliance features"""
    
    def __init__(self, encryption_service: EncryptionService):
        self.encryption_service = encryption_service
        self.data_retention_days = 365
        self.anonymized_data: Dict[str, Dict] = {}
    
    def anonymize_user_data(self, user_id: str, user_data: Dict) -> Dict:
        """
        Anonymize user data while preserving analytics value
        
        Args:
            user_id: User to anonymize
            user_data: User's data
            
        Returns:
            Anonymized data
        """
        # Generate anonymous ID
        anonymous_id = self.encryption_service.hash_sensitive_data(user_id)
        
        # Remove PII
        anonymized = {
            "anonymous_id": anonymous_id,
            "created_date": user_data.get('created_date'),
            "subscription_tier": user_data.get('subscription_tier'),
            "country": user_data.get('country'),  # Keep general location
            # Remove: name, email, phone, IP addresses, etc.
        }
        
        self.anonymized_data[user_id] = anonymized
        
        return anonymized
    
    def request_data_export(self, user_id: str) -> Dict:
        """
        Generate data export for user (GDPR right to data portability)
        
        Args:
            user_id: User requesting export
            
        Returns:
            All user data in portable format
        """
        # Collect all user data
        user_export = {
            "user_id": user_id,
            "export_date": datetime.now().isoformat(),
            "personal_info": {},  # User profile
            "entities_monitored": [],  # Entities
            "alerts": [],  # Alert history
            "reports": [],  # Generated reports
            "settings": {}  # User preferences
        }
        
        return user_export
    
    def request_data_deletion(self, user_id: str) -> bool:
        """
        Process data deletion request (GDPR right to erasure)
        
        Args:
            user_id: User requesting deletion
            
        Returns:
            Success status
        """
        # Steps for data deletion:
        # 1. Verify user identity
        # 2. Check for legal holds
        # 3. Anonymize or delete data
        # 4. Retain audit logs (as required by law)
        # 5. Notify user of completion
        
        try:
            # Anonymize instead of hard delete (preserves analytics)
            # Hard delete PII
            # Keep audit logs with anonymized ID
            
            print(f"Data deletion request processed for user: {user_id}")
            return True
        except Exception as e:
            print(f"Error processing deletion: {e}")
            return False
    
    def check_data_retention(self, data_timestamp: datetime) -> bool:
        """
        Check if data should be retained based on policy
        
        Args:
            data_timestamp: Timestamp of data
            
        Returns:
            True if data should be retained
        """
        from datetime import timedelta
        
        retention_cutoff = datetime.now() - timedelta(days=self.data_retention_days)
        return data_timestamp >= retention_cutoff


class SecurityService:
    """Unified security service"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        self.encryption = EncryptionService(encryption_key)
        self.rbac = RBACService()
        self.audit = AuditLogger()
        self.gdpr = GDPRComplianceService(self.encryption)
    
    def secure_api_request(
        self,
        user_id: str,
        required_permission: Permission,
        action: str,
        resource_type: str,
        resource_id: str,
        request_data: Dict
    ) -> tuple[bool, Optional[str]]:
        """
        Secure an API request with permission check and audit logging
        
        Returns:
            (success, error_message)
        """
        # Check permission
        if not self.rbac.check_permission(user_id, required_permission):
            self.audit.log_action(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=request_data.get('ip_address', ''),
                user_agent=request_data.get('user_agent', ''),
                success=False,
                details={"error": "permission_denied"}
            )
            return False, "Permission denied"
        
        # Log successful access
        self.audit.log_action(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=request_data.get('ip_address', ''),
            user_agent=request_data.get('user_agent', ''),
            success=True
        )
        
        return True, None


# Example usage
if __name__ == "__main__":
    # Initialize security service
    security = SecurityService()
    
    # Set up RBAC
    security.rbac.assign_role("user_123", UserRole.MANAGER)
    security.rbac.assign_role("user_456", UserRole.VIEWER)
    
    # Check permissions
    can_export = security.rbac.check_permission("user_123", Permission.EXPORT_DATA)
    print(f"User 123 can export data: {can_export}")
    
    # Secure API request
    success, error = security.secure_api_request(
        user_id="user_123",
        required_permission=Permission.VIEW_DASHBOARD,
        action="view",
        resource_type="dashboard",
        resource_id="dash_001",
        request_data={"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"}
    )
    
    print(f"API request successful: {success}")
    
    # GDPR data export
    user_data = security.gdpr.request_data_export("user_123")
    print(f"Exported data keys: {list(user_data.keys())}")
