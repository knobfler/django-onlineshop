from django.contrib import admin

# Register your models here.
from shop.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # name필드를 참조하여 slug필드는 자동으로 만들어줘라
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    # 자주바뀌는 목록들
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Product, ProductAdmin)