import csv
from django.core.management.base import BaseCommand
from blog.models import Post  # Import your Post model


class Command(BaseCommand):
    help = 'Exports all blog posts to a CSV file'

    def handle(self, *args, **kwargs):
        # Define the CSV file path
        file_path = 'blog_posts_export.csv'

        # Get all blog posts
        posts = Post.objects.all()

        # Specify the fields to export
        fields = [
            'title', 'slug', 'author', 'featured_image',
            'alt_text', 'image_credit', 'content', 'excerpt',
            'created_on', 'updated_on', 'status', 'publish_date',
            'viewed_by', 'views', 'seo_tags', 'meta_description'
        ]

        # Write to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(fields)  # Write the header row

            for post in posts:
                # Prepare row data
                row = [
                    post.title,
                    post.slug,
                    # Export author's username instead of the user object
                    post.author.username,
                    post.featured_image.url if post.featured_image else '',
                    post.alt_text,
                    post.image_credit,
                    post.content,
                    post.excerpt,
                    post.created_on,
                    post.updated_on,
                    post.status,
                    post.publish_date,
                    # List of viewers' usernames
                    ', '.join(
                        [user.username for user in post.viewed_by.all()]),
                    post.views,
                    post.seo_tags,
                    post.meta_description,
                ]
                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully exported {posts.count()} blog posts to {file_path}'))
