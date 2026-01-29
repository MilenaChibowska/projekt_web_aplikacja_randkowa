import copy
from rest_framework import permissions

class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user

        if hasattr(obj, 'owner'):
            return obj.owner.user == request.user
            
        return False