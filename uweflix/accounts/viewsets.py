from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .serializers import ModuleSerializer
from accounts.models import *
from accounts.permissions import *

class ModelViewSet(ModelViewSet):
    """
    ModuleViewSet that provides the default `list`, `create`, `retrieve`, `update` and `destroy` actions for the Module model.

    Endpoints:
    GET /api/modules/ - List all modules
    POST /api/modules/ - Create a new module
    GET /api/modules/<pk>/ - Retrieve a module
    PUT /api/modules/<pk>/ - Update a module
    PATCH /api/modules/<pk>/ - Partially update a module
    DELETE /api/modules/<pk>/ - Delete a module
    """
    queryset = User.objects.all()
    serializer_class = ModuleSerializer
    # Define the default permission classes for the ModuleViewSet
    # These actions can only be done if the user is the following UserTypes
    permission_classes = [IsAccountsManager]

    def get_permissions(self):
        return super().get_permissions()

    def get_permissions(self):
        """
        Override the default permissions for the ModuleViewSet
        to allow authenticated users to access the `list` and
        `retrieve` actions. But only admin users can access the `create`, `update`, and `destroy` actions.
        """
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()