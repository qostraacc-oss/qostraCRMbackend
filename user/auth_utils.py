from .auth_core import GenericJWTAuthentication
from .services import crm_user_sync_service

class CRMJWTAuthentication(GenericJWTAuthentication):
    """
    CRM-specific JWT Authentication.
    Uses CRMUserSyncService to handle user registration/caching.
    """
    @property
    def sync_service(self):
        return crm_user_sync_service

# For backward compatibility with settings.py if needed, 
# though we should update settings.py to point to CRMJWTAuthentication
JWTAuthentication = CRMJWTAuthentication
