from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(
            owner=self.request.user,
            is_archived=False

        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def archive(self, request,pk=None):
        budget = self.get_object()
        budget.is_archived = True
        budget.save()
        return Response({'status': 'archivé'})


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(budget__owner=self.request.user)

    def perform_create(self, serializer):
        budget_id = self.request.data.get("budget")
        budget = Budget.objects.get(
        id=budget_id, owner=self.request.user)
        serializer.save(budget=budget)