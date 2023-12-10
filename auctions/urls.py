from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts, name="posts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("listing/<int:auction_id>/comment", views.comment, name="comment"),
    path("listing/<int:auction_id>/addWatchlist/", views.addWatchlist, name="addWatchlist"),
    path("listing/<int:auction_id>/removeWatchlist/", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<int:auction_id>/get_comments/", views.get_comments, name="get_comments"),
    path("account_settings/", views.accountSettings, name="account_settings")
]
