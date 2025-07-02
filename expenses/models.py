from django.db import models
from users.models import CustomUser
from uuid import uuid4

class Expense(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    date = models.DateTimeField(blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    
    class CurrencyChoices(models.TextChoices):
        CEDIS = "CEDIS",
        DOLLARS = "DOLLARS"
        
    currency = models.CharField(choices=CurrencyChoices, default=CurrencyChoices.CEDIS)
    reimbursable = models.BooleanField(default=False)
    
    class CategoryChoices(models.TextChoices):
        TRIP = "Trip"
        SERVICES = "Services"
        CATERING = "Catering"
        
    category = models.CharField(choices=CategoryChoices, default=CategoryChoices.SERVICES)
    description = models.TextField()

