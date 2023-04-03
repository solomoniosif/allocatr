from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .mixins import HtmxOnlyMixin, HtmxTemplateResponseMixin, RequirePostMixin


class HtmxTemplateView(HtmxTemplateResponseMixin, TemplateView):
    """A TemplateView that renders a partial template
    if the request is sent by HTMX or a full page otherwise."""


class HtmxOnlyTemplateView(HtmxOnlyMixin, TemplateView):
    """A TemplateView that only responds to HTMX requests.

    This view is intended to be used for html fragments that are going to be
    inserted by HTMX into an already loaded page."""


class HtmxDetailView(HtmxTemplateResponseMixin, DetailView):
    """A DetailView that renders a partial template if the request is sent by HTMX
    or a full page otherwise."""


class HtmxOnlyDetailView(HtmxOnlyMixin, DetailView):
    """A DetailView that only responds to HTMX requests.

    This view is intended to be used for html fragments that are going to be
    inserted by HTMX into an already loaded page."""


class HtmxListView(HtmxTemplateResponseMixin, ListView):
    """A ListView that renders a partial template if the request is sent by HTMX
    or a full page otherwise."""


class HtmxOnlyListView(HtmxOnlyMixin, ListView):
    """A ListView that only responds to HTMX requests.

    This view is intended to be used for html fragments that are going to be
    inserted by HTMX into an already loaded page."""


class HtmxCreateView(HtmxTemplateResponseMixin, CreateView):
    """A CreateView that renders a partial template if the request is sent by HTMX
    or a full page otherwise."""


class HtmxOnlyCreateView(HtmxOnlyMixin, CreateView):
    """A CreateView that only responds to HTMX requests.

    This view is intended to be used for html fragments that are going to be
    inserted by HTMX into an already loaded page."""


class HtmxUpdateView(HtmxTemplateResponseMixin, UpdateView):
    """A UpdateView that renders a partial template if the request is sent
    by HTMX or a full page otherwise.""" ""


class HtmxOnlyUpdateView(HtmxOnlyMixin, UpdateView):
    """A UpdateView that only responds to HTMX requests.

    This view is intended to be used for html fragments that are going to be
    inserted by HTMX into an already loaded page."""


class HtmxDeleteView(RequirePostMixin, DeleteView):
    pass


class HtmxOnlyDeleteView(HtmxOnlyMixin, RequirePostMixin, DeleteView):
    pass
