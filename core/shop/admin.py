from django.contrib import admin

from .models import Category, Product

# type hinting imports
from django.http import HttpRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category Model Admin
    """
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)
    
    def  get_prepopulated_fields(self, request: HttpRequest, obj=None) -> dict:
        """Returns a dictionary of fields to pre-populate from the request."""
        return {
            'slug': ('name',),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product Model Admin
    """
    list_display = ('title', 'brand', 'price', 'discount', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    ordering = ('title',)

    def  get_prepopulated_fields(self, request: HttpRequest, obj=None) -> dict:
        """Returns a dictionary of fields to pre-populate from the request."""
        return {
            'slug': ('title',),
        }