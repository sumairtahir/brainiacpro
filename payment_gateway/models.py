import pytz
from django.db import models
from authentication.models import Account
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    tokens = models.IntegerField(default=0)
    is_expirable = models.IntegerField(default=0)
    bg_image = models.ImageField(upload_to="products/bg_image", blank=True)

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Subscription(models.Model):
    user = models.ForeignKey(Account, related_name="subscriptions", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    is_expirable = models.IntegerField(default=0)
    expiry = models.DateTimeField(default=None, null=True)
    is_expired = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=256, default=0)
    tokens = models.IntegerField(default=0)
    is_completed = models.IntegerField(default=0)
    is_verified = models.IntegerField(default=0)

    def expire_subscription(self):
        current = pytz.utc.localize(datetime.now())
        if self.expiry < current and self.is_expirable and self.is_expired == 0:
            self.user.tokens = 0
            self.is_expired = 1
            self.save()
            self.user.save()
