from rest_framework.permissions import BasePermission 

 

class IsAdmin(BasePermission): 

    def has_permission(self, request, view): 

        return request.user.is_authenticated and request.user.role == 'admin' 

 

class IsManager(BasePermission): 

    def has_permission(self, request, view): 

        return request.user.is_authenticated and request.user.role in ['admin', 'manager'] 

 

class IsEmployee(BasePermission): 

    def has_permission(self, request, view): 

        return request.user.is_authenticated and request.user.role in ['admin', 'manager', 'employee'] 