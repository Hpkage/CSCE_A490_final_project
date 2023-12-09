from django.contrib import admin

from auctions.models import User, Auction, Comment, Watchlist
# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Watchlist)

