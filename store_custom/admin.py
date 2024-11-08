from store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem

# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields=['tag']
    model = TaggedItem
    extra = 0

class customProductAdmin(ProductAdmin):
    inlines = [TagInline]
    
admin.site.unregister(Product)
admin.site.register(Product, customProductAdmin)