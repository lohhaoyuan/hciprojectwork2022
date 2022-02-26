from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("@",views.user_search, name="users"),
    path("@/<str:username>", views.profile, name="profile"),
    path("@/<str:username>/edit", views.profile_edit, name="editprofile"),
    path("search",views.search, name="search")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
