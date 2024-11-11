from django.contrib import admin
from .models import Product, Purchase
# from notes.models import Note
from django_summernote.admin import SummernoteModelAdmin


# Product Admin View
class ProductAdmin(SummernoteModelAdmin):
    # Apply Summernote to these fields
    summernote_fields = ('content', 'excerpt',)
    # removed stock and tier refs
    list_display = ('title', 'slug', 'price', 'category')
    search_fields = ('title', 'content')
    ordering = ('title',)
    # Auto Generates slug from title
    prepopulated_fields = {'slug': ('title',)}
    # Adds a UI widget for ManyToManyField
    filter_horizontal = ('related_products',)


# Purchase Admin View
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity',
                    'price_paid', 'purchase_date', 'status')
    list_filter = ('status', 'purchase_date')
    search_fields = ('user__username', 'product__title')
    ordering = ('-purchase_date',)


# Register the models with the custom views
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
