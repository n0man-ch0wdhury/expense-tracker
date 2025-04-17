from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, TransactionViewSet,
    BudgetViewSet, MonthlySummaryView, DashboardView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]