from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Category, Transaction, Budget

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'type', 'is_default')
    
    def create(self, validated_data):
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'category', 'category_name', 'description', 'date', 'type', 'created_at')
        read_only_fields = ('created_at',)
    
    def create(self, validated_data):
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent_amount = serializers.DecimalField(source='get_spent_amount', read_only=True, max_digits=10, decimal_places=2)
    remaining_amount = serializers.DecimalField(source='get_remaining_amount', read_only=True, max_digits=10, decimal_places=2)
    percentage_used = serializers.FloatField(source='get_percentage_used', read_only=True)
    
    class Meta:
        model = Budget
        fields = ('id', 'category', 'category_name', 'amount', 'month', 'year', 
                 'spent_amount', 'remaining_amount', 'percentage_used')
    
    def create(self, validated_data):
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['remaining_balance'] = data['total_income'] - data['total_expense']
        return data