from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("budgets", views.BudgetViewSet, basename="budget")
router.register("transactions", views.TransactionViewSet, basename="transaction")

urlpatterns = router.urls
