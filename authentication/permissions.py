from rest_framework.permissions import BasePermission


class SignUpPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous and \
                request.method == "POST":
            return True
        else:
            return False


class CovidDataPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and \
                request.method == "GET":
            return True
        else:
            return False
