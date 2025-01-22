from io import BytesIO
from typing import cast, Optional, Union, Any

import wrapt
from django.http import HttpRequest, HttpResponse, QueryDict
from django.urls import path, reverse, ResolverMatch, resolve

from hyperpony.htmx import swap_oob
from hyperpony.response_handler import RESPONSE_HANDLER, add_response_handler
from hyperpony.utils import response_to_str


# @deprecated("use embedded API")
# class IsolatedRequest(wrapt.ObjectProxy):
#     @classmethod
#     def wrap(cls, request: HttpRequest):
#         return IsolatedRequest(request)
#
#     @property
#     def method(self):
#         return "GET"
#
#     @property
#     def GET(self):
#         return QueryDict()
#
#     @property
#     def POST(self):
#         return QueryDict()
#
#     @property
#     def FILES(self):
#         return MultiValueDict()


# class ViewResponse(wrapt.ObjectProxy):
#     def __str__(self):
#         response = cast(HttpResponse, self)
#         response_string = text_response_to_str_or_none(response)
#         return response_string if response_string is not None else super().__str__()
#
#     def as_response(self) -> HttpResponse:
#         return cast(HttpResponse, self)


# @deprecated("use CBV")
# def view(
#     *,
#     decorators: Optional[list[Callable]] = None,
#     login_required=False,
#     inject_params=True,
# ) -> Callable[[VIEW_FN], VIEW_FN]:
#     if decorators is None:
#         decorators = []
#
#     if login_required:
#         decorators = [auth_decorators.login_required(), *decorators]
#
#     def decorator(fn: VIEW_FN) -> VIEW_FN:
#         if inject_params:
#             fn = hyperpony.inject_params()(fn)
#
#         if decorators is not None:
#             for d in reversed(decorators):
#                 fn = d(fn)
#
#         @functools.wraps(fn)
#         def inner(*args, **kwargs) -> HttpResponse:
#             view_request: HttpRequest = args[0]
#             try:
#                 response = fn(view_request, *args[1:], **kwargs)
#                 response = (
#                     ViewResponse(response) if not isinstance(response, ViewResponse) else response
#                 )
#                 return response
#             finally:
#                 pass
#
#         return cast(VIEW_FN, view_stack()(inner))
#
#     return decorator


# @deprecated("use embedded API")
# @method_decorator(view_stack(), name="dispatch")
# class NestedView(views.View):
#     """
#     Attributes:
#         isolate_request:
#             Only applies when this view is rendered via the `as_str()` method.
#             If True, `request.GET`, `request.POST` and `request.FILES` will be empty.
#             If False, the request object will get passed through without change.
#     """
#
#     isolate_request: bool
#     __is_child_view: bool
#
#     def __init__(self, **kwargs):
#         self.__is_child_view = False
#
#         # subclasses may set this as a class attribute
#         # make sure not to override it then
#         if not hasattr(self, "isolate_request"):
#             self.isolate_request = True
#         super().__init__(**kwargs)
#
#     @property
#     def is_child_view(self):
#         """
#         Returns True, if this view was rendered with the `as_str()` method.
#         """
#         return self.__is_child_view
#
#     def as_str(
#         self,
#         request: HttpRequest,
#         *args,
#         **kwargs,
#     ):
#         """
#         Returns the response's body as string if the content type is text, otherwise
#         the default string representation of the response.
#
#         By default, `request.GET`, `request.POST` and `request.FILES` will be empty.
#         See `isolate_request` for more details.
#         """
#         self.__is_child_view = True
#         if self.isolate_request:
#             request = IsolatedRequest.wrap(request)
#
#         self.setup(request, *args, **kwargs)
#         response = self.dispatch(request, *args, **kwargs)
#         response_string = text_response_to_str_or_none(response)
#         return response_string if response_string is not None else str(response)


def is_head(request: HttpRequest) -> bool:
    return request.method == "HEAD"


def is_get(request: HttpRequest) -> bool:
    return request.method == "GET"


def is_post(request: HttpRequest) -> bool:
    return request.method == "POST"


def is_put(request: HttpRequest) -> bool:
    return request.method == "PUT"


def is_patch(request: HttpRequest) -> bool:
    return request.method == "PATCH"


def is_delete(request: HttpRequest) -> bool:
    return request.method == "DELETE"


class ViewUtilsMixin:
    def is_get(self):
        """
        Returns True, if the request method is GET.
        """
        return self.request.method == "GET"  # type: ignore

    def is_post(self):
        """
        Returns True, if the request method is POST.
        """
        return self.request.method == "POST"  # type: ignore

    def is_put(self):
        """
        Returns True, if the request method is PUT.
        """
        return self.request.method == "PUT"  # type: ignore

    def is_patch(self):
        """
        Returns True, if the request method is PATCH.
        """
        return self.request.method == "PATCH"  # type: ignore

    def is_delete(self):
        """
        Returns True, if the request method is DELETE.
        """
        return self.request.method == "DELETE"  # type: ignore

    def url(self):
        rm = self.request.resolver_match  # type: ignore
        return reverse(rm.view_name, args=rm.args, kwargs=rm.kwargs)

    def add_response_handler(self, handler: RESPONSE_HANDLER):
        """
        Add a response handler.
        """
        add_response_handler(self.request, handler)  # type: ignore

    def add_swap_oob(
        self,
        additional: HttpResponse | list[HttpResponse],
        hx_swap_oob_method="outerHTML",
    ):
        self.add_response_handler(
            lambda response: swap_oob(response, additional, hx_swap_oob_method)
        )

    def is_embedded_view(self):
        return is_embedded_request(self.request)  # type: ignore


class SingletonPathMixin:
    @classmethod
    def get_path_name(cls) -> Optional[str]:
        return cls.__dict__.get("__path_name", None)

    @classmethod
    def create_path(cls, path_start: Optional[str] = None, path_end=""):
        path_name = cls.get_path_name()
        if path_name is not None:
            raise Exception("create_path() can only be called once per view class.")
        if path_start is None:
            path_start = cls.__name__
        if path_start[-1] != "/":
            path_start += "/"
        route_path = path_start + path_end

        path_name = f"{cls.__module__}.{cls.__name__}".replace(".", "-")
        setattr(cls, "__path_name", path_name)

        return path(route_path, cast(Any, cls).as_view(), name=path_name)

    # noinspection PyPep8Naming
    @classmethod
    def embed(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        *args,
        **kwargs,
    ):
        path_name = cls.get_path_name()
        if path_name is None:
            raise Exception(f"View {cls} was not registered with create_path().")
        return embed_view(request, path_name, args=args, kwargs=kwargs, GET=GET)

    # noinspection PyPep8Naming
    @classmethod
    def invoke(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        *args,
        **kwargs,
    ):
        path_name = cls.get_path_name()
        if path_name is None:
            raise Exception(f"View {cls} was not registered with create_path().")
        return invoke_view(request, path_name, args=args, kwargs=kwargs, GET=GET)

    # noinspection PyPep8Naming
    @classmethod
    def swap_oob(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        hx_swap="outerHTML",
        *args,
        **kwargs,
    ):
        self_response = cls.invoke(request, GET, *args, **kwargs)
        add_response_handler(
            request,
            lambda response: swap_oob(response, self_response, hx_swap),
        )

    @classmethod
    def reverse(cls, urlconf=None, args=None, kwargs=None, current_app=None):
        return reverse(
            cls.get_path_name(), urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
        )


class EmbeddedRequest(wrapt.ObjectProxy):
    def __init__(self, original_request: HttpRequest):
        super().__init__(original_request)
        self.__original_request = original_request

    @property
    def scheme(self):
        return self.__original_request.scheme


def create_embedded_request(original_request: HttpRequest):
    embedded_req = HttpRequest()
    setattr(embedded_req, "__hyperpony_embedded_request", True)

    embedded_req._read_started = False  # noqa: SLF001
    embedded_req._stream = BytesIO()  # noqa: SLF001

    embedded_req.COOKIES = original_request.COOKIES
    embedded_req.META = original_request.META
    embedded_req.content_type = "text/html; charset=utf-8"
    embedded_req.content_params = {}
    embedded_req.method = "GET"

    return embedded_req


# noinspection PyPep8Naming
def invoke_view(
    request: HttpRequest,
    view_name: str,
    GET: Union[QueryDict, dict, None] = None,  # noqa: N803
    *,
    args=None,
    kwargs=None,
    urlconf=None,
    current_app=None,
) -> HttpResponse:
    if isinstance(GET, dict):
        get_qd = QueryDict(mutable=True)
        get_qd.update(GET)
    elif GET is None:
        get_qd = QueryDict()
    else:
        get_qd = GET

    embedded_req = create_embedded_request(request)
    embedded_req.GET = get_qd
    embedded_req.POST = QueryDict()

    url = reverse(view_name, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    rm: ResolverMatch = resolve(url, urlconf=urlconf)
    embedded_req.path = rm.route
    embedded_req.path_info = rm.route
    embedded_req.resolver_match = rm

    embedded_req = EmbeddedRequest(embedded_req)

    response = rm.func(embedded_req, *rm.args, **rm.kwargs)
    return response


# noinspection PyPep8Naming
def embed_view(
    request: HttpRequest,
    view_name: str,
    GET: Union[QueryDict, dict, None] = None,  # noqa: N803
    *,
    urlconf=None,
    args=None,
    kwargs=None,
    current_app=None,
):
    response = invoke_view(
        request,
        view_name=view_name,
        urlconf=urlconf,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
        GET=GET,
    )
    return response_to_str(response)


def is_embedded_request(request: HttpRequest) -> bool:
    return getattr(request, "__hyperpony_embedded_request", False)


class ElementIdMixin:
    element_id: Optional[str] = None

    def get_element_id(self) -> str:
        return self.element_id or self.__class__.__name__


class ElementAttrsMixin:
    def get_attrs(self) -> dict[str, str]:
        return {}
