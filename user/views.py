from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import OnboardingService

class GetStartedView(APIView):
    """
    Initializes CRM-specific data like workspace and onboarding state.
    """
    def post(self, request):
        user_info = request.user
        if not user_info or not hasattr(user_info, 'user_id'):
            return Response(
                {"error": "User not identified or authenticated."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        onboarding_data = request.data
        result = OnboardingService.initialize_onboarding(user_info, onboarding_data)
        
        if result['status'] == 'already_onboarded':
            return Response(
                {"message": "User already onboarded.", "user_id": user_info.user_id},
                status=status.HTTP_200_OK
            )

        return Response({
            "message": "Onboarding successful.",
            "workspace": {
                "name": result['workspace'].name,
                "slug": result['workspace'].slug
            },
            "user": {
                "user_id": user_info.user_id,
                "is_onboarded": user_info.is_onboarded
            }
        }, status=status.HTTP_201_CREATED)

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD for Products, isolated to the authenticated user.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Only return products belonging to the authenticated UserInfo
        return Product.objects.filter(user_info=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the product to the authenticated UserInfo
        serializer.save(user_info=self.request.user)
