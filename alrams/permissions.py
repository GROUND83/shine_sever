from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, alram):
        return bool(alram.to == request.user)
