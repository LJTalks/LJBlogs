from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    # Added seo_list status to see if it has data
    list_display = ('title', 'slug', 'status', 'created_on', 'seo_tags_status')
    search_fields = ['title', 'content', 'seo_tags']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Custom method to display if seo_tags is empty or not
    def seo_tags_status(self, obj):
        return "Yes" if obj.seo_tags else "No"

    # Adding a short description for the list view column
    seo_tags_status.short_description = 'SEO Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'approved',
                    'created_on')  # Columns in the comment list
    # Add filters for approval status and creation date
    list_filter = ('approved', 'created_on')
    # Allow searching by username and comment content
    search_fields = ('author_username', 'body')
    actions = ['approve_comments']  # Custom action to bulk approve comments

    # Custom action to approve selected comments
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"
