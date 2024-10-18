from rest_framework.permissions import BasePermission

class IsTaxiDriver(BasePermission):
    """
    Custom permission to only allow taxi drivers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Taxi Driver").exists()

class IsCustomer(BasePermission):
    """
    Custom permission to only allow customers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Customer").exists()
