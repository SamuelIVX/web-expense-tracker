from django.contrib import admin
from .models import Category, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'monthly_budget')

from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'amount', 'tx_date', 'created_at')
    list_filter = ('category', 'tx_date')
    search_fields = ('user__username', 'note')
    list_select_related = ('user', 'category')
