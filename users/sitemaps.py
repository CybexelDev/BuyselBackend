from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    priority_mapping = {
        'home': 1.0,
        'about': 0.8,
        'register': 0.8,
        'blog': 0.8,
        'faq': 0.8,
        'services': 0.8,
        'contact': 0.8,
    }

    def items(self):
        return self.priority_mapping.keys()

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priority_mapping[item]
