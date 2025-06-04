from django.contrib.sitemaps import Sitemap
from .models import BlogPost  # Your blog post model

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # or obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()
