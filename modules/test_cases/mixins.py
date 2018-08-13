from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class GroupRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.group:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)