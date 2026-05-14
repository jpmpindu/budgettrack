from dataclasses import field
from rest_framework import serializers
from .models import Budget, Transaction, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    class Meta:
        model = Transaction
        fields = ['id', 'label', 'amount', 'type', 'date', 'category', 'category_name']

class BudgetSerializer(serializers.ModelSerializer):
    transactions    =TransactionSerializer(many=True, read_only=True)
    total_expenses  =serializers.SerializerMethodField()
    total_income    = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ['id', 'name', 'month', 'limit', 'is_archived', 'created_at', 'transactions', 'total_expenses', 'total_income' ]
        read_only_fields = ['created_at']

    def get_total_expenses(self, obj):
        return sum(t.amount for t in obj.transactions.all() if t.type == 'expense')

    def get_total_income(self, obj):
        return sum(t.amount for t in obj.transactions.all() if t.type == "income")

    def validate_limit(self, value):
        if value <= 0:
            raise serializers.ValidationError('La limite doit être supérieure à 0.')
