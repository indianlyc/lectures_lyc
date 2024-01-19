from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "datetime"
    list_display = ["datetime", "title"]

# admin.site.register(Post, PostAdmin)