from django.contrib import admin

from auctions.models import Auction, Comment, Watchlist
# Register your models here.
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Watchlist)
