from django.contrib import admin, messages
from django.http import HttpRequest
from django.db.models import QuerySet, Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

class inventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', "LOW")
                ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    list_display = ('title','unit_price', 'inventory_status', 'collection_title')
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', inventoryFilter]
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title__istartswith']
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering="inventory")
    def inventory_status(self, status):
        if status.inventory < 10:
            return "LOW"
        else:
            return "OK"

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, 
                          f"{updated_count} products were succefully updated", 
                          messages.ERROR)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_counts']
    search_fields =['title']
    
    @admin.display(ordering="product_counts")
    def product_counts(self, count):
        url = (reverse('admin:store_product_changelist')
               + "?" + urlencode({
                   'collection__id': str(count.id)
               }))
        return format_html('<a href="{}">{}</a>', url,  count.product_counts)

    def get_queryset(self, request: HttpRequest)-> QuerySet:
        return super().get_queryset(request).annotate(product_counts = Count('productcollection'))

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership', 'ordered')
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    @admin.display(ordering='ordered')
    def ordered(self, custom_order):
        url = (reverse('admin:store_order_changelist')
               + "?"+urlencode({
                   'order__id': custom_order.id
               }))
        return format_html('<a href="{}">{}</a>', url, custom_order.ordered)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(ordered=Count('order'))

# class OrderItemInline(admin.TabularInline):
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10
    model = models.Orderitem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines =[OrderItemInline]
    list_display = ["id", "customer", "placed_at", "payment_status"]
    list_per_page = 10
    ordering = ["id","customer", "placed_at"]