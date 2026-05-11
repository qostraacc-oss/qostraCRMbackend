from django.utils.text import slugify
from .models import UserInfo, Workspace
from .auth_core import BaseUserSyncService

class CRMUserSyncService(BaseUserSyncService):
    """
    CRM-specific implementation of user synchronization.
    """
    @property
    def model(self):
        return UserInfo

    def update_local_user(self, user_instance, token_payload):
        updated = False
        if 'email' in token_payload and user_instance.email != token_payload['email']:
            user_instance.email = token_payload['email']
            updated = True
        
        # Add more CRM-specific field mapping here
        return updated

# Instance to be used by the Auth class
crm_user_sync_service = CRMUserSyncService()

class OnboardingService:
    @staticmethod
    def initialize_onboarding(user_info, data=None):
        """
        Initializes CRM-specific data for a new user.
        """
        if user_info.is_onboarded:
            return {"status": "already_onboarded", "user_info": user_info}

        # 1. Create Default Workspace
        workspace_name = (data or {}).get('workspace_name', f"{user_info.user_id}'s Workspace")
        base_slug = slugify(workspace_name)
        slug = base_slug
        counter = 1
        while Workspace.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        workspace = Workspace.objects.create(
            owner=user_info,
            name=workspace_name,
            slug=slug,
            is_default=True
        )

        # 2. Update Onboarding State
        user_info.is_onboarded = True
        user_info.onboarding_step = 'COMPLETED'
        user_info.save()

        return {
            "status": "success",
            "workspace": workspace,
            "user_info": user_info
        }
