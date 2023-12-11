from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts, name="posts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.logout_view, name="profile"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("listing/<int:auction_id>/comment", views.comment, name="comment"),
    path("listing/<int:auction_id>/addWatchlist/", views.addWatchlist, name="addWatchlist"),
    path("listing/<int:auction_id>/removeWatchlist/", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<int:auction_id>/get_comments/", views.get_comments, name="get_comments"),
    path("account_settings/", views.accountSettings, name="account_settings"),
    path('about_us/', views.aboutUs, name="about_us"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)