# ruff: noqa: F401
from django.views import View as DjangoView

from .client_state import ClientStateView
from .element import ElementResponse, ElementView
from .inject_params import param, InjectParamsMixin
from .views import SingletonPathMixin, ViewUtilsMixin


class HyperponyView(ViewUtilsMixin, InjectParamsMixin, DjangoView):
    pass


class HyperponyElementView(ViewUtilsMixin, InjectParamsMixin, ClientStateView, ElementView):
    pass
