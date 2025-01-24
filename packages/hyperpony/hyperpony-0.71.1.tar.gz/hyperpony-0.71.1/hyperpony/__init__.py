# ruff: noqa: F401
from django.views import View as DjangoView

from .client_state import ClientStateMixin
from .element import ElementResponse, ElementMixin
from .inject_params import param, InjectParamsMixin
from .views import SingletonPathMixin, ViewUtilsMixin


class HyperponyMixin(InjectParamsMixin, ViewUtilsMixin):
    pass


class HyperponyElementMixin(InjectParamsMixin, ClientStateMixin, ElementMixin, ViewUtilsMixin):
    pass
