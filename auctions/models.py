from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"User id: {self.id} | Username: {self.username}"

    def get_username(self):
        return self.username


# define the model of a auction list
class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    image = models.ImageField(upload_to= 'images/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_seller")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Auction id: {self.id} | Title: {self.title} | Seller: {self.seller}"
    
    def get_fields(self):
        return [(field.name, getattr(self, field.name)) for field in Auction._meta.fields]


# define the model of a comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    message = models.TextField(blank=False)
    cm_date = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_comments")

    def __str__(self):
        return f"{self.user} comments on {self.auction}"


# define the model of a watchlist
class Watchlist(models.Model):
    auctions = models.ManyToManyField(Auction, related_name="auctions_in_watchlist", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user}'s watchlist"