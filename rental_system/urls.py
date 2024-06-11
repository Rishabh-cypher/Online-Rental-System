from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from base_app.views import (
    home_view,
    login_view,
    logout_view,
    register_view,
    admin_renter_register_requests_list_view,
    handle_create_renter_register_request,
    handle_reject_register_request,
    handle_accept_register_request,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path(
        "renter/register_as_renter/",
        handle_create_renter_register_request,
        name="create_register_as_renter",
    ),
    path(
        "pwuser/renter_requests/",
        admin_renter_register_requests_list_view,
        name="admin_renter_register_list",
    ),
    path(
        "pwuser/renter_requests/reject/",
        handle_reject_register_request,
        name="admin_renter_register_reject",
    ),
    path(
        "pwuser/renter_requests/accept/",
        handle_accept_register_request,
        name="admin_renter_register_accept",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
