from django.contrib.auth.models import AbstractUser
from django.db import models

CURRENCIES = [ 
  ('USD', 'USD'), 
  ('EUR', 'EUR')
]

class User(AbstractUser):
  pass

class Listing(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
  title = models.CharField(max_length=64)
  description = models.TextField()
  category = models.CharField(max_length=10)
  image_url = models.URLField(blank=True)
  cents = models.DecimalField(max_digits=9, decimal_places=2)
  currency = models.CharField(max_length=3, choices=CURRENCIES)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.title} created in {self.category} category by {self.user} for {self.cents}"

class Bid(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
  cents = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.cents} {self.currency} for {self.listing}"

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user} commented on {self.listing}: {self.body}"