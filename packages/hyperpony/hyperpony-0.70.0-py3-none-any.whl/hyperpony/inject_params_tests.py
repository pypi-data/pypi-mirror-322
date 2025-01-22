from typing import Optional

import orjson.orjson
import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import path
from django.views import View
from django.views.generic import TemplateView

from hyperpony import param
from hyperpony.inject_params import InjectParamsMixin
from hyperpony.testutils import view_from_response
from hyperpony.utils import response_to_str
from hyperpony.views import invoke_view


# #######################################################################
# ### CBVs
# #######################################################################


class ViewWithSelfInResponse(View):
    def dispatch(self, request, *args, **kwargs):
        res = HttpResponse("")
        res.view = self
        return res


class TViewP1(InjectParamsMixin, ViewWithSelfInResponse):
    p1: str = param("aaa")

    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(self.p1)


urlpatterns = [
    path("tviewp1/", TViewP1.as_view(), name="tviewp1"),
]


#######################################################################
### common views
#######################################################################


def test_without_type_annotation(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1 = param()  # type: ignore
        p2 = param()  # type: ignore

    view = view_from_response(V, V.as_view()(rf.get("/?p1=123&p2=456")))
    assert view.p1 == "123"
    assert view.p2 == "456"


def test_missing_param_raises_exception(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: str = param()

    with pytest.raises(Exception):
        V.as_view()(rf.get(""))


def test_inject_params_simple_view(rf: RequestFactory):
    rs = response_to_str(TViewP1.as_view()(rf.get("/?p1=abc")))
    assert rs == "abc"


def test_inject_params_values_can_be_passed_with_kwargs(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: str = param("aaa")
        p2: int = param(123)

    view = view_from_response(V, V.as_view(p1="bbb", p2=456)(rf.get("/")))
    assert view.p1 == "bbb"
    assert view.p2 == 456


@pytest.mark.urls("hyperpony.inject_params_tests")
def test_inject_params_request_is_isolated_by_default(rf: RequestFactory):
    rs = response_to_str(invoke_view(rf.post("/?p1=bbb"), "tviewp1"))
    assert rs == "aaa"


def test_inject_params_template_view(rf: RequestFactory):
    class V(InjectParamsMixin, TemplateView):
        template_name = "hyperpony/tests/TemplateResponse.html"
        p1: str = param()

        def get_context_data(self, **kwargs):
            assert self.p1 == "aaa"
            return {"foo": "bar"}

    V.as_view()(rf.get("/?p1=aaa"))


def test_inject_params_json_body(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: str = param("aaa")
        p2: int = param(123)

    data = orjson.dumps({"p1": "bbb", "p2": 456})
    view = view_from_response(
        V, V.as_view()(rf.post("/", data=data, content_type="application/json"))
    )
    assert view.p1 == "bbb"
    assert view.p2 == 456


#######################################################################
### default values
#######################################################################


def test_inject_params_default_values(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: str = param("aaa")
        p2: int = param(123)

    view = view_from_response(V, V.as_view()(rf.get("/")))
    assert view.p1 == "aaa"
    assert view.p2 == 123


def test_inject_params_default_values_are_overridden_by_query_args(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: str = param("aaa")
        p2: int = param(123)

    view = view_from_response(V, V.as_view()(rf.get("/?p1=bbb")))
    assert view.p1 == "bbb"
    assert view.p2 == 123


def test_param_default_defines_target_type(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1 = param(123)

    view = view_from_response(V, V.as_view()(rf.get("/?p1=999")))
    assert view.p1 == 999


#######################################################################
### optional
#######################################################################


def test_optional(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: Optional[str] = param()

    view = view_from_response(V, V.as_view()(rf.get("/")))
    assert view.p1 is None


# def test_optional_as_union(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str | None = param()):
#         assert p1 is None
#
#     viewfn(rf.get("/"))
#
#
# def test_optional_as_union_with_default_none(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str | None = param(None)):
#         assert p1 is None
#
#     viewfn(rf.get("/"))
#
#
# def test_optional_with_type_conversion(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: Optional[int] = param()):
#         assert p1 == 1
#
#     viewfn(rf.get("/?p1=1"))


#######################################################################
### type conversions
#######################################################################


def test_inject_params_type_conversion_list_annotated(rf: RequestFactory):
    class V(InjectParamsMixin, ViewWithSelfInResponse):
        p1: list[int] = param()

    view = view_from_response(V, V.as_view()(rf.get("/?p1=1&p1=2")))
    assert isinstance(view.p1, list)
    assert 1 in view.p1
    assert 2 in view.p1


#######################################################################
### function-based views
#######################################################################


#
#
# def test_type_conversion_int(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: int = param()):
#         assert p1 == 1
#
#     viewfn(rf.get("/?p1=1"))
#
#
# def test_type_conversion_with_exception(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: int | ValueError = param()):
#         assert isinstance(p1, ValueError)
#
#     viewfn(rf.get("/?p1=a"))
#
#
# def test_type_conversion_float(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: float = param()):
#         assert p1 == 1.1
#         # assert type(p1) == float
#         assert isinstance(p1, float)
#
#     viewfn(rf.get("/?p1=1.1"))
#
#
# def test_type_conversion_bool(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: bool = param(), p2: bool = param(), p3: bool = param()):
#         assert not p1
#         assert not p2
#         assert not p3
#
#     viewfn(rf.get("/?p1=false&p2=False&p3"))
#
#
# def test_type_conversion_list_unannotated(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: list = param()):
#         assert isinstance(p1, list)
#         assert "a" in p1
#         assert "b" in p1
#
#     viewfn(rf.get("/?p1=a&p1=b"))
#
#
# def test_type_conversion_list_annotated(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: list[int] = param()):
#         assert isinstance(p1, list)
#         assert 1 in p1
#         assert 2 in p1
#
#     viewfn(rf.get("/?p1=1&p1=2"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: AppUser = param()):
#         assert user is not None
#
#     app_user = AppUser.objects.create(username="testuser")
#     viewfn(rf.get(f"/?user={app_user.id}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_wrong_id_object_does_not_exist_type(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: AppUser | ObjectDoesNotExist = param()):
#         assert isinstance(user, ObjectDoesNotExist)
#
#     viewfn(rf.get(f"/?user={uuid4()}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_wrong_id_object_does_not_exist__with_pktype(
#     rf: RequestFactory,
# ):
#     wrong_id = uuid4()
#
#     @inject_params()
#     def viewfn(_request, user: AppUser | ObjectDoesNotExistWithPk = param()):
#         assert isinstance(user, ObjectDoesNotExistWithPk)
#         assert user.pk == str(wrong_id)
#
#     viewfn(rf.get(f"/?user={wrong_id}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_wrong_id_model_does_not_exist_type(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: AppUser | AppUser.DoesNotExist = param()):  # type: ignore
#         assert isinstance(user, AppUser.DoesNotExist)
#
#     viewfn(rf.get(f"/?user={uuid4()}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_with_optional(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: Optional[AppUser] = param()):
#         assert user is not None
#
#     app_user = AppUser.objects.create(username="testuser")
#     viewfn(rf.get(f"/?user={app_user.id}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_with_optional_value_is_none(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: Optional[AppUser] = param()):
#         assert user is None
#
#     viewfn(rf.get("/"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_with_union_none(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: AppUser | None = param()):
#         assert user is not None
#
#     app_user = AppUser.objects.create(username="testuser")
#     viewfn(rf.get(f"/?user={app_user.id}"))
#
#
# @pytest.mark.django_db
# def test_type_conversion_model_with_union_none_value_is_none(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, user: AppUser | None = param()):
#         assert user is None
#
#     viewfn(rf.get("/"))
#
#
# def test_post(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str = param(methods=["POST"]), p2: str = param(methods=["POST"])):
#         assert p1 == "a"
#         assert p2 == "b"
#
#     viewfn(rf.post("/", {"p1": "a", "p2": "b"}))
#
#
# def test_patch(rf: RequestFactory):
#     @inject_params()
#     def viewfn(
#         _request,
#         p1: str = param(methods=["PATCH"]),
#         p2: str = param(methods=["PATCH"]),
#     ):
#         assert p1 == "aaa"
#         assert p2 == "bbb"
#
#     viewfn(
#         rf.patch(
#             "/",
#             urlencode({"p1": "aaa", "p2": "bbb"}),
#             content_type="application/x-www-form-urlencoded",
#         )
#     )
#
#
# def test_get_and_post_order(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str = param()):
#         assert p1 == "a"
#
#     viewfn(rf.post("/?p1=a", {"p1": "b"}))
#
#
# def test_function_call_arg_overrides_param(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str = param()):
#         assert p1 == "b"
#
#     viewfn(rf.get("/?p1=a"), "b")
#
#
# def test_function_call_kwarg_overrides_param(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str = param()):
#         assert p1 == "b"
#
#     viewfn(rf.get("/?p1=a"), p1="b")
#
#
# def test_param_view_stack(rf: RequestFactory):
#     @inject_params()
#     def view1(request, p1: str = param()):
#         assert p1 == "a"
#         return view2(request)
#
#     @inject_params()
#     def view2(request, p1: str = param(default="b")):
#         assert p1 == "b"
#
#     view1(rf.get("/?p1=a"))
#
#
# def test_auto_default_value(rf: RequestFactory):
#     @inject_params()
#     def viewfn(_request, p1: str = param(default="a")):
#         assert p1 == "a"
#
#     untyped_viewfn = typing.cast(Any, viewfn)
#     untyped_viewfn(rf.get("/"))
#
