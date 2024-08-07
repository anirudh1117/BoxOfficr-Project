from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = "You do not have permission to perform action"
    permission_map = {
        "GET": "{app_label}.view_{model_name}",
        "POST": "{app_label}.add_{model_name}",
        "PUT": "{app_label}.change_{model_name}",
        "PATCH": "{app_label}.change_{model_name}",
        "DELETE": "{app_label}.delete_{model_name}",
    }

    def _get_permission(self, method, perm_slug):
        app, model = perm_slug.split(".")
        if method not in self.permission_map:
            raise MethodNotAllowed(method)
        perm = self.permission_map.get(method).format(app_label=app, model_name=model)
        return perm

    def has_permission(self, request, view):
        perm = self._get_permission(
            method=request.method, perm_slug=view.perm_slug
        )
        if request.user.has_perm(perm):
            #print(list(request.user.user_permissions.all()))
            #print(request.user.is_superuser)
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            print(obj.author)
            return True
        return False