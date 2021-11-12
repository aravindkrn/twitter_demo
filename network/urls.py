from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("myposts/", views.my_posts, name="my_posts"),
    path("api/posts/", views.PostApiView.as_view()),
    path("api/user/<str:username>/", views.UserApiView.as_view()),
    path("healthifyMe/", views.healthifyMe)
]
