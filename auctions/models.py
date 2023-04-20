from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    
    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    
    NEW, USED = "NEW", "USED"
    condition_choices = ((NEW, "new"), (USED, "used"))
    condition = models.CharField(max_length=4, choices=condition_choices, default=NEW)
    
    img_URL = models.URLField(default="https://d1csarkz8obe9u.cloudfront.net/posterpreviews/bjj-logo-design-template-20f626b12d9207649f81a24f4ce48308_screen.jpg?ts=1678120477")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="seller")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    details = models.TextField(max_length=600, default="No details available.")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}"
    

class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.item.name} - {self.offer}€ by {self.bidder.username}"
    

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True, default="No title")
    content = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.title} "
    
    
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)    
    
    def __str__(self):
        return f"{self.item.name} on {self.user.username} watchlist"
    