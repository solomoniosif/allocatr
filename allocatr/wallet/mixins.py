from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import BadRequest, ImproperlyConfigured, PermissionDenied
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateResponseMixin


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


class HtmxTemplateResponseMixin(TemplateResponseMixin):
    htmx_template_name = None

    def get_template_names(self):
        super().get_template_names()

        if self.template_name is None or self.htmx_template_name is None:
            raise ImproperlyConfigured(
                "HtmxTemplateResponseMixin requires either a definition of both "
                "'template_name' and 'htmx_template_name' or an override of "
                "'get_template_names()'"
            )

        if self.request.headers.get("HX-Request"):
            return [self.htmx_template_name]
        return [self.template_name]


class HtmxOnlyMixin:
    """
    Mixin to ensure that the view can only be accessed via HX-Request.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            raise BadRequest("This view can only be accessed via HX-Request")
        return super().dispatch(request, *args, **kwargs)
