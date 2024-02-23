from django.db.models.base import Model
from django.template.defaultfilters import truncatewords_html
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.safestring import SafeText
import markdown
from .models import Post

class LatestPostFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy("blog:post_list")
    description = "New Posts of My Blog"
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title 
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish
    
    def item_enclosure_url(self, item):
        return item.picture.url
    
    def item_enclosure_mime_type(self, item):
        return "image/jpeg"
    
       