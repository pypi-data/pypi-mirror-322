from typing import cast

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import re_path, path
from django.views import View

from hyperpony import ViewUtilsMixin, SingletonPathMixin
from hyperpony.testutils import view_from_response
from hyperpony.utils import response_to_str, text_response_to_str_or_none
from hyperpony.views import invoke_view, is_embedded_request


# #######################################################################
# ### CBVs
# #######################################################################


class TView(ViewUtilsMixin, View):
    def dispatch(self, request, *args, **kwargs):
        res = HttpResponse("")
        res.view = self
        return res


class TViewSingleton(SingletonPathMixin, TView):
    pass


class TViewSingletonPathStart(TViewSingleton):
    pass


class TViewSingletonPathEnd(TViewSingleton):
    pass


class TViewSingletonPathEndParam(TViewSingleton):
    pass


class TViewSingletonPathStartPathEnd(TViewSingleton):
    pass


urlpatterns = [
    path("view1/", TView.as_view(), name="view1"),
    re_path("view1/<param1>", TView.as_view(), name="view1_param"),
    TViewSingleton.create_path(),
    TViewSingletonPathStart.create_path("custom_start"),
    TViewSingletonPathEnd.create_path(None, "custom_end"),
    TViewSingletonPathEndParam.create_path(None, "<param1>"),
    TViewSingletonPathStartPathEnd.create_path("custom_start", "<param1>"),
]


# #######################################################################
# ### text_response_to_str
# #######################################################################


def test_text_response_to_str_or_none():
    assert response_to_str(HttpResponse("response")) == "response"


def test_text_response_to_str_or_none_content_type_json():
    res = HttpResponse("{}", content_type="application/json")
    assert text_response_to_str_or_none(res) is None


# #######################################################################
# ### embedded request
# #######################################################################


@pytest.mark.urls("hyperpony.views_tests")
def test_is_embedded_request(rf: RequestFactory):
    view = view_from_response(TView, invoke_view(rf.get("/"), "view1"))
    assert is_embedded_request(view.request)


@pytest.mark.urls("hyperpony.views_tests")
def test_viewutil_is_embedded_request(rf: RequestFactory):
    view = view_from_response(TView, invoke_view(rf.post("/"), "view1"))
    assert view.is_embedded_view()


@pytest.mark.urls("hyperpony.views_tests")
def test_embedded_view_request_is_always_get(rf: RequestFactory):
    view = view_from_response(TView, invoke_view(rf.post("/"), "view1"))
    assert view.is_get()


def test_viewutils_http_methods(rf: RequestFactory):
    assert view_from_response(TView, TView.as_view()(rf.get("/"))).is_get()
    assert view_from_response(TView, TView.as_view()(rf.post("/"))).is_post()
    assert view_from_response(TView, TView.as_view()(rf.put("/"))).is_put()
    assert view_from_response(TView, TView.as_view()(rf.patch("/"))).is_patch()
    assert view_from_response(TView, TView.as_view()(rf.delete("/"))).is_delete()


# #######################################################################
# ### ViewUtils
# #######################################################################


@pytest.mark.urls("hyperpony.views_tests")
def test_viewutils_url(rf: RequestFactory):
    assert view_from_response(ViewUtilsMixin, invoke_view(rf.post("/"), "view1")).url() == "/view1/"

    res = invoke_view(rf.get("/"), cast(str, TViewSingleton.get_path_name()))
    assert view_from_response(ViewUtilsMixin, res).url() == "/TViewSingleton/"

    res = invoke_view(rf.get("/"), cast(str, TViewSingletonPathStart.get_path_name()))
    assert view_from_response(ViewUtilsMixin, res).url() == "/custom_start/"

    res = invoke_view(rf.get("/"), cast(str, TViewSingletonPathEnd.get_path_name()))
    assert view_from_response(ViewUtilsMixin, res).url() == "/TViewSingletonPathEnd/custom_end"

    pn = cast(str, TViewSingletonPathEndParam.get_path_name())
    res = invoke_view(rf.get("/"), pn, kwargs={"param1": "foo"})
    assert view_from_response(ViewUtilsMixin, res).url() == "/TViewSingletonPathEndParam/foo"

    pn = cast(str, TViewSingletonPathStartPathEnd.get_path_name())
    res = invoke_view(rf.get("/"), pn, kwargs={"param1": "foo"})
    assert view_from_response(ViewUtilsMixin, res).url() == "/custom_start/foo"
