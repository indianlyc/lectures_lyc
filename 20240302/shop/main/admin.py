from django.contrib import admin

from .models import Category, Good

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "category", "img"]