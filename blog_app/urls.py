from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Blog CRUD
    path("create/", views.create_post, name="create_post"),

    path("post/<int:id>/", views.post_detail, name="post_detail"),

    path("update/<int:id>/", views.update_post, name="update_post"),

    path("delete/<int:id>/", views.delete_post, name="delete_post"),


    # Authentication
    path("register/", views.register, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="blog_app/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # Profile
    path(
    "profile/<int:id>/",
    views.profile,
    name="profile"
),


    # Likes
    path(
        "like/<int:id>/",
        views.like_post,
        name="like_post"
    ),


    # Category
    path(
        "category/<int:id>/",
        views.category_posts,
        name="category_posts",
    ),
    path(
        "like/<int:id>/",
        views.like_post,
        name="like_post"
    ),


    # Password Reset
     path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

]