class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    priority_mapping = {
        'index': 1.0,         # Corrected from 'home'
        'faq': 0.8,
        'blog': 0.8,
        'agents': 0.8,
        'more': 0.8,
        'properties': 0.8,
        'agent_form': 0.8,
        'property_form': 0.8,
    }

    def items(self):
        return self.priority_mapping.keys()

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priority_mapping[item]
