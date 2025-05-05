from rest_framework.permissions import BasePermission

class IsNutricionista(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_nutricionista
    
class IsPaciente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_paciente