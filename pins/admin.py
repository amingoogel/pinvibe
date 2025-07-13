from django.contrib import admin
from .models import Pin, Comment, Like, Category
from users.models import Follow

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'board', 'created_at', 'like_count', 'comment_count']
    list_filter = ['category', 'board', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['category', 'board']
    readonly_fields = ['created_at']

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pin', 'user', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'user__username']
    readonly_fields = ['created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['pin', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['pin__title', 'user__username']
    readonly_fields = ['created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['created_at']