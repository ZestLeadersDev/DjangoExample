from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'slug', 'author', 'publish', 'status')
    list_filter         = ('status', 'created', 'publish', 'author')
    search_fields       = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)} # autofills slug field
    raw_id_fields       = ('author',) # nice search in post
    date_hierarchy      = 'publish'
    ordering            = ('status', 'publish')
