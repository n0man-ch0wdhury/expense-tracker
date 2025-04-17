import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for all users or a specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to create default categories for (optional)'
        )

    def handle(self, *args, **options):
        # Default income categories
        default_income_categories = [
            'Salary',
            'Freelance',
            'Investments',
            'Gifts',
            'Other Income'
        ]

        # Default expense categories
        default_expense_categories = [
            'Housing',
            'Food',
            'Transportation',
            'Utilities',
            'Healthcare',
            'Entertainment',
            'Shopping',
            'Education',
            'Personal Care',
            'Debt Payments',
            'Savings',
            'Other Expenses'
        ]

        # Get username from options
        username = options.get('username')

        # If username is provided, create categories for that user only
        if username:
            try:
                user = User.objects.get(username=username)
                self._create_categories_for_user(user, default_income_categories, default_expense_categories)
                self.stdout.write(self.style.SUCCESS(f'Successfully created default categories for user {username}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
        else:
            # Create categories for all users
            users = User.objects.all()
            for user in users:
                self._create_categories_for_user(user, default_income_categories, default_expense_categories)
            
            # Also create default categories (not associated with any user)
            self._create_default_categories(default_income_categories, default_expense_categories)
            
            self.stdout.write(self.style.SUCCESS('Successfully created default categories for all users'))

    def _create_categories_for_user(self, user, income_categories, expense_categories):
        # Create income categories
        for category_name in income_categories:
            Category.objects.get_or_create(
                name=category_name,
                type='income',
                user=user,
                defaults={'is_default': False}
            )

        # Create expense categories
        for category_name in expense_categories:
            Category.objects.get_or_create(
                name=category_name,
                type='expense',
                user=user,
                defaults={'is_default': False}
            )

    def _create_default_categories(self, income_categories, expense_categories):
        # Create default income categories (not associated with any user)
        for category_name in income_categories:
            Category.objects.get_or_create(
                name=category_name,
                type='income',
                user=None,
                defaults={'is_default': True}
            )

        # Create default expense categories (not associated with any user)
        for category_name in expense_categories:
            Category.objects.get_or_create(
                name=category_name,
                type='expense',
                user=None,
                defaults={'is_default': True}
            )