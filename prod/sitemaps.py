from django.contrib.sitemaps import Sitemap
from .models import TngProducts

class TngprodSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return TngProducts.objects.all()
    
    # def lastmod(self,obj):
    #     return obj.Name