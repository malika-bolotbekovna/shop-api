from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsAnonymous(BasePermission):
    
    def has_permission(self, request, view):
        return request.method != "POST"
    

class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff and request.method != "POST"