from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import Product, Purchase
# from notes.models import Note
from django_summernote.admin import SummernoteModelAdmin


# Product Admin View
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'excerpt',)
    list_display = ('title', 'slug', 'price', 'category',
                    'get_status_display')
    search_fields = ('title', 'content')
    ordering = ('title',)
    # Auto Generates slug from title
    prepopulated_fields = {'slug': ('title',)}
    # Adds a UI widget for ManyToManyField
    filter_horizontal = ('related_products',)

    # Define the action for duplicating products
    actions = ['duplicate_product']

    def duplicate_product(self, request, queryset):
        for product in queryset:
            # Create a new instance of the product
            product_copy = Product.objects.get(pk=product.pk)
            product_copy.pk = None  # This creates a new object instead of updating the existing one
            product_copy.title = f"{product.title} (Copy)"
            product_copy.slug = f"{product.slug}-copy"
            product_copy.save()
        self.message_user(request, "Selected products have been duplicated.")

    duplicate_product.short_description = "Duplicate selected products"

    # Add a custom button in the admin view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('duplicate/<int:product_id>/', self.admin_site.admin_view(
                self.duplicate_single_product), name="duplicate_product"),
        ]
        return custom_urls + urls

    def duplicate_single_product(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        product_copy = Product.objects.get(pk=product.pk)
        product_copy.pk = None
        product_copy.title = f"{product.title} (Copy)"
        product_copy.slug = f"{product.slug}-copy"
        product_copy.save()
        self.message_user(request, f"{product.title} has been duplicated.")
        return redirect("admin:products_product_changelist")

    def duplicate_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Duplicate</a>',
            f"{obj.id}/duplicate/"
        )

    duplicate_button.short_description = "Duplicate Button"
    duplicate_button.allow_tags = True

    list_display = ('title', 'slug', 'price', 'category', 'get_status_display')


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
