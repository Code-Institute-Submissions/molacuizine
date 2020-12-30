from django.contrib import admin
from .models import Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # Admin display
    list_display = (
        'name',
        'category',
        'price',
        'image',
    )
    # Ordering in admin
    ordering = ('id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# The model followed by class name (model, class name)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)