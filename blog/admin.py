from django.contrib import admin
from .models import Post, BlogComment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    # Added seo_list status to see if it has data
    # fields to display in the admin panel for the Post model
    list_display = ('title', 'slug', 'status', 'created_on', 'publish_date',
                    'seo_tags_status')
    search_fields = ['title', 'content', 'seo_tags']
    list_filter = ('status', 'created_on', 'publish_date')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Custom method to display if seo_tags is empty or not
    def seo_tags_status(self, obj):
        return "Yes" if obj.seo_tags else "No"

    # Adding a short description for the list view column
    seo_tags_status.short_description = 'SEO Tags'

    # Manually set publish date in admin panel
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'featured_image',
                       'content', 'excerpt', 'status', 'publish_date')
        }),
    )


# Customise the BlogComment admin interface
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'status',
                    'created_on', 'updated_on')  # Cols in the comment list
    # Filters for approval status and creation date
    list_filter = ('created_on', 'status')
    # Allow searching by username and blogcomment content
    search_fields = ('author__username', 'body')
    # Custom action to bulk approve comments
    actions = ['approve_blog_comments']

    # Custom action to approve selected comments
    def approve_blog_comments(self, request, queryset):
        queryset.update(status=1)
    # Custom action short description 
    approve_blog_comments.short_description = "Approve selected comments"
