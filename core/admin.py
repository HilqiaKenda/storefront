from core.models import User
from store.models import Product
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductimageInline
from tags.models import TaggedItem

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "first_name", "last_name"),
            }),
        )

class TagInline(GenericTabularInline):
    autocomplete_fields=['tag']
    model = TaggedItem
    extra = 0

class customProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductimageInline]
    
admin.site.unregister(Product)
admin.site.register(Product, customProductAdmin)