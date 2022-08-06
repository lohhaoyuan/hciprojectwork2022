from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("@", views.user_search, name="users"),
    path("@/<str:username>", views.profile, name="profile"),
    path("@/<str:username>/edit", views.profile_edit, name="editprofile"),
    path("search", views.search, name="search"),
    path("error418", views.error418, name="error418"),
    path("important/notice", views.rick, name="rick"),
    path("new/", views.make_post, name="make_post"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("delete/<int:post_id>", views.delete, name="delete"),
    path("documentation", views.documentation, name="documentation"),
    path("following", views.following, name="following"),
    path('postsearch', views.post_search, name="post_search"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
