from django.contrib import admin
from .models import Post, Comment
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


# Register your models here.
admin.site.register(Comment)


# I think this doesn't work because we used a CBV for comment model?
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('author', 'body', 'post', 'approved',
#                     'created_on', 'updated_on')  # Cols in the comment list
#     # Add filters for approval status and creation date
#     list_filter = ('approved', 'created_on', 'status')
#     # Allow searching by username and comment content
#     search_fields = ('author_username', 'body')
#     actions = ['approve_comments']  # Custom action to bulk approve comments

#     # Custom action to approve selected comments
#     def approve_comments(self, request, queryset):
#         queryset.update(approved=True)
# /workspace/LJBlogs/static/images
#     approve_comments.short_description = "Approve selected comments"
