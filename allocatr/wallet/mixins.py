from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


class OwnerOnlyPermission(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()  # noqa
        if not obj.user == request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RequirePostMixin:
    """
    Mixin to ensure that the view can only be accessed via HTTP POST method.
    """

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return require_POST(view)
