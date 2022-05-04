from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, complaints):
        print(complaints)
        return bool(complaints.author == request.user)
