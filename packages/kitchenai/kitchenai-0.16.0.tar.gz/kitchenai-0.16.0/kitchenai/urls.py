import djp
from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from falco_toolbox import views as toolbox_views
from health_check.views import MainView
import django_eventstream

from .api import api

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path("api/", api.urls),
    path(".well-known/security.txt", toolbox_views.security_txt),
    path("robots.txt", toolbox_views.robots_txt),
    path("", RedirectView.as_view(pattern_name="dashboard:home"), name="home"),
    path("health/", MainView.as_view()),
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("dashboard/", include("kitchenai.dashboard.urls", namespace="dashboard")),
    #path("events/", include(django_eventstream.urls)) #TODO: Uncomment this when we have a streaming endpoint
] + djp.urlpatterns()

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
