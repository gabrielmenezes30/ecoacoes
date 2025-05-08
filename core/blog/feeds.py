from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post  # seu modelo de postagem

class LatestPostsFeed(Feed):
    title = "Últimas postagens do Blog"
    link = "/rss/"
    description = "Acompanhe as últimas postagens sobre sustentabilidade."

    def items(self):
        return Post.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:200]  # resumo

    def item_link(self, item):
        return reverse('post_detail', args=[item.slug])
