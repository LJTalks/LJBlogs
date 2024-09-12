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


# Register your models here.
admin.site.register(Comment)
