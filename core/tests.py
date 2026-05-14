from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Budget, Transaction, Category
from decimal import Decimal

# Create your tests here.

class BudgetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.bob = User.objects.create_user(
            username="bob", password="motdepasse123"
        )

        self.alice = User.objects.create_user(username="alice", password="motdepasse123")

        self.budget_alice = Budget.objects.create(
            owner=self.alice,
            name="Budget Mai",
            month="2026-05-01",
            limit=Decimal("2000.00"),
        )

        self.budget_bob = Budget.objects.create(
            owner=self.bob,
            name="Budget Juin",
            month="2026-06-01",
            limit=Decimal("15000.00"),
        )

    def test_bob_ne_voit_pas_budget_alice(self):
        self.client.force_authenticate(user=self.bob)
        response = self.client.get(f"/api/budgets/{self.budget_alice.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_creer_budget_limite_negative(self):
        self.client.force_authenticate(user=self.alice)
        data = {"name": "Invalide", "month": "2026-06-01", "limit": "-500.00"}
        response = self.client.post("/api/budgets/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)