from calendar import month
from random import choices
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='circle')

    def __str__(self):
        return self.name

class Budget (models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name        = models.CharField(max_length=200)
    month       = models.DateField()
    limit       = models.DecimalField(max_digits=10, decimal_places=2)
    is_archived = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    INCOME, EXPENSE = 'income', 'expense'
    TYPE_CHOICES = [(INCOME, 'Revenu'), (EXPENSE, 'Dépense')]

    budget      = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    label       = models.CharField(max_length=200)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    type        = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date        = models.DateField()