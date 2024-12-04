from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Q

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

    def has_pending_order(self):
        """
        Ensures that the user has no more than one pending order.
        """
        return self.orders.filter(status='Pending').exists()
    
    @property
    def full_name(self):
        """ Returns the user's full name """
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status == 'Pending' and self.user.has_pending_order():
            raise ValueError("A user can have only one pending order at a time.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"