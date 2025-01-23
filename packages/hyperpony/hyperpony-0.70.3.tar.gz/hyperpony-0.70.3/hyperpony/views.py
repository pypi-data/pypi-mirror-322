from io import BytesIO
from typing import cast, Optional, Union, Any

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


class DispatchToGetOnAllMethodsMixin:
    def get(self, request, *args, **kwargs):
        raise Exception(f"GET method handler not implemented for this view {self}.")

    def post(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)


class SingletonPathMixin:
    @classmethod
    def get_path_name(cls) -> Optional[str]:
        return cls.__dict__.get("__path_name", None)

    @classmethod
    def create_path(
        cls,
        path_suffix: Optional[str] = None,
        *,
        full_path: Optional[str] = None,
        name: Optional[str] = None,
    ):
        if cls.get_path_name() is not None:
            raise Exception("create_path() can only be called once per view class.")
        if full_path is not None and path_suffix is not None:
            raise Exception("Either full_path or path_suffix can be specified, not both.")

        if full_path is None:
            path_suffix = "" if path_suffix is None else path_suffix
            full_path = cls.__name__
            full_path += "/" if len(path_suffix) > 0 and not path_suffix.startswith("/") else ""
            full_path += path_suffix

        path_name = (
            name if name is not None else f"{cls.__module__}.{cls.__name__}".replace(".", "-")
        )
        setattr(cls, "__path_name", path_name)

        return path(full_path, cast(Any, cls).as_view(), name=path_name)

    # noinspection PyPep8Naming
    @classmethod
    def embed(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        POST: Union[QueryDict, dict, None] = None,  # noqa: N803
        *args,
        **kwargs,
    ):
        path_name = cls.get_path_name()
        if path_name is None:
            raise Exception(f"View {cls} was not registered with create_path().")
        return embed_view(request, path_name, GET=GET, POST=POST, args=args, kwargs=kwargs)

    # noinspection PyPep8Naming
    @classmethod
    def invoke(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        POST: Union[QueryDict, dict, None] = None,  # noqa: N803
        *args,
        **kwargs,
    ):
        path_name = cls.get_path_name()
        if path_name is None:
            raise Exception(f"View {cls} was not registered with create_path().")
        return invoke_view(request, path_name, GET=GET, POST=POST, args=args, kwargs=kwargs)

    # noinspection PyPep8Naming
    @classmethod
    def swap_oob(
        cls,
        request: HttpRequest,
        GET: Union[QueryDict, dict, None] = None,  # noqa: N803
        POST: Union[QueryDict, dict, None] = None,  # noqa: N803
        hx_swap="outerHTML",
        *args,
        **kwargs,
    ):
        self_response = cls.invoke(request, GET=GET, POST=POST, args=args, kwargs=kwargs)
        add_response_handler(
            request,
            lambda response: swap_oob(response, self_response, hx_swap),
        )

    @classmethod
    def reverse(cls, urlconf=None, args=None, kwargs=None, current_app=None):
        return reverse(
            cls.get_path_name(), urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
        )


class EmbeddedRequest(HttpRequest):
    @classmethod
    def create(
        cls,
        original_request: HttpRequest,
        get: Optional[QueryDict] = None,
        post: Optional[QueryDict] = None,
    ):
        self = cls()
        self.__original_request = original_request
        self._read_started = False
        self._stream = BytesIO()
        self.COOKIES = original_request.COOKIES
        self.META = original_request.META
        self.content_type = "text/html; charset=utf-8"
        self.content_params = {}
        self.method = "GET" if post is None else "POST"
        self.GET = cast(Any, get) if get is not None else QueryDict()
        self.POST = cast(Any, post) if post is not None else QueryDict()
        return self

    def __getattr__(self, name):
        return getattr(self.__original_request, name)


# noinspection PyPep8Naming
def invoke_view(
    request: HttpRequest,
    view_name: str,
    GET: Union[QueryDict, dict, None] = None,  # noqa: N803
    POST: Union[QueryDict, dict, None] = None,  # noqa: N803
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
    if isinstance(POST, dict):
        post_qd = QueryDict(mutable=True)
        post_qd.update(POST)
    else:
        post_qd = POST

    embedded_req = EmbeddedRequest.create(request, get_qd, post_qd)

    url = reverse(view_name, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    rm: ResolverMatch = resolve(url, urlconf=urlconf)
    embedded_req.path = rm.route
    embedded_req.path_info = rm.route
    embedded_req.resolver_match = rm

    response = rm.func(embedded_req, *rm.args, **rm.kwargs)
    return response


# noinspection PyPep8Naming
def embed_view(
    request: HttpRequest,
    view_name: str,
    GET: Union[QueryDict, dict, None] = None,  # noqa: N803
    POST: Union[QueryDict, dict, None] = None,  # noqa: N803
    *,
    args=None,
    kwargs=None,
    urlconf=None,
    current_app=None,
):
    response = invoke_view(
        request,
        view_name=view_name,
        GET=GET,
        POST=POST,
        args=args,
        kwargs=kwargs,
        urlconf=urlconf,
        current_app=current_app,
    )
    return response_to_str(response)


def is_embedded_request(request: HttpRequest) -> bool:
    return isinstance(request, EmbeddedRequest)


class ElementIdMixin:
    element_id: Optional[str] = None

    def get_element_id(self) -> str:
        return self.element_id or self.__class__.__name__


class ElementAttrsMixin:
    def get_attrs(self) -> dict[str, str]:
        return {}
