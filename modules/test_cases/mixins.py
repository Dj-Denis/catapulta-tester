from django.contrib.auth.mixins import AccessMixin


class GroupRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.group:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)