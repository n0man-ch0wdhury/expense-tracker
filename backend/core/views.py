from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from .models import Category, Transaction, Budget
from .serializers import (
    UserSerializer, CategorySerializer, TransactionSerializer,
    BudgetSerializer, MonthlySummarySerializer
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Only allow users to see their own profile
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()
    
    def get_permissions(self):
        # Allow anyone to register, but only authenticated users for other actions
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'type']
    
    def get_queryset(self):
        # Return user's custom categories and default categories
        return Category.objects.filter(
            (Q(user=self.request.user) | Q(is_default=True))
        ).distinct()
    
    @action(detail=False, methods=['get'])
    def income(self, request):
        # Filter categories by income type
        queryset = self.get_queryset().filter(type='income')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expense(self, request):
        # Filter categories by expense type
        queryset = self.get_queryset().filter(type='expense')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'category__name', 'type']
    
    def get_queryset(self):
        # Return only user's transactions
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Filter by transaction type if provided
        transaction_type = self.request.query_params.get('type')
        if transaction_type in ['income', 'expense']:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category if provided
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def income(self, request):
        # Filter transactions by income type
        queryset = self.get_queryset().filter(type='income')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expense(self, request):
        # Filter transactions by expense type
        queryset = self.get_queryset().filter(type='expense')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only user's budgets
        queryset = Budget.objects.filter(user=self.request.user)
        
        # Filter by month and year if provided
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month and year:
            queryset = queryset.filter(month=month, year=year)
        elif year:
            queryset = queryset.filter(year=year)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        # Get current month's budgets
        today = timezone.now().date()
        queryset = self.get_queryset().filter(month=today.month, year=today.year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get month and year from query params or use current month
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not month or not year:
            today = timezone.now().date()
            month = today.month
            year = today.year
        
        # Calculate total income and expenses for the month
        income = Transaction.objects.filter(
            user=request.user,
            type='income',
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense = Transaction.objects.filter(
            user=request.user,
            type='expense',
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Create summary data
        summary = {
            'month': int(month),
            'year': int(year),
            'total_income': income,
            'total_expense': expense,
            'remaining_balance': income - expense
        }
        
        serializer = MonthlySummarySerializer(summary)
        return Response(serializer.data)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get current date
        today = timezone.now().date()
        
        # Get monthly summary
        income = Transaction.objects.filter(
            user=request.user,
            type='income',
            date__month=today.month,
            date__year=today.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense = Transaction.objects.filter(
            user=request.user,
            type='expense',
            date__month=today.month,
            date__year=today.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get recent transactions
        recent_transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-date', '-created_at')[:5]
        
        # Get budgets for current month
        budgets = Budget.objects.filter(
            user=request.user,
            month=today.month,
            year=today.year
        )
        
        # Prepare response data
        data = {
            'summary': {
                'month': today.month,
                'year': today.year,
                'total_income': income,
                'total_expense': expense,
                'remaining_balance': income - expense
            },
            'recent_transactions': TransactionSerializer(recent_transactions, many=True).data,
            'budgets': BudgetSerializer(budgets, many=True).data
        }
        
        return Response(data)