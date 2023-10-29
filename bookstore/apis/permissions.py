from rest_framework import permissions

# create custom permissions to use in rest_framework

class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            """ returns if owner of review is logged in user"""
            return obj.reviewer == request.user
        

class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        """ returns true if it is a get request
        if it is not a get request checks if the user is admin or not"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
        
