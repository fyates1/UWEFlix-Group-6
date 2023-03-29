from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import User

class IsCustomer(IsAuthenticated):
    """
    Custom permission to only allow customers to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.userType == User.UserType.CUSTOMER)

class IsStudent(IsAuthenticated):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.userType == User.UserType.STUDENT)

class IsClubRep(IsAuthenticated):
    """
    Custom permission to only allow club reps to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.userType == User.UserType.CLUBREP)

class IsAccountsManager(IsAuthenticated):
    """
    Custom permission to only allow accounts managers to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.userType == User.UserType.ACCOUNTSMANAGER)

class IsCinemaManager(IsAuthenticated):
    """
    Custom permission to only allow cinema managers to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.userType == User.UserType.CINEMAMANAGER)
