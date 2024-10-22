from django.contrib import admin
from .models import Post, BlogComment
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # Load custom JS for autosave
    class Media:
        js = ('js/autosave.js',)

    # Added seo_list status to see if it has data
    # fields to display in the admin panel for the Post model
    list_display = ('title', 'slug', 'status', 'created_on', 'publish_date',
                    'seo_tags_status', 'meta_description',
                    'meta_description_with_fallback')
    search_fields = ['title', 'content', 'seo_tags']
    list_filter = ('status', 'created_on', 'publish_date')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    # Custom action to bulk publish posts
    actions = ['publish_blog_posts']
    
    # Auto save posts as draft if status isn't manually set
    def save_model(self, request, obj, form, change):
        if not obj.status:
            obj.status = 0
        super().save_model(request, obj, form, change)

    # Custom action to publish selected posts
    def publish_blog_posts(self, request, queryset):
        queryset.update(status=1)
        
    # Custom action short description
    publish_blog_posts.short_description = "Publish blog posts"

    # Custom method to display if seo_tags is empty or not
    def seo_tags_status(self, obj):
        return "Yes" if obj.seo_tags else "No"

    # Adding a short description for the list view column
    seo_tags_status.short_description = 'SEO Tags'
    
    # Filter author dropdown staff only
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Manually set publish date in admin panel
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'author',
                'featured_image',
                'alt_text',
                'image_credit',
                'content',
                'excerpt',
                'status',
                'publish_date',
                'seo_tags',
                'meta_description',
            )
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
