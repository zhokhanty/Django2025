from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'ADMIN'

class IsTrader(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'TRADER'

class IsSalesRep(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'SALES_REP'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'CUSTOMER'
