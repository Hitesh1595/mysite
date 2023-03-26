import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html

from django.urls import reverse_lazy

from blog.models import Post

# subclassing the  feed class of the syndication framework
class LatestPostsFeed(Feed):
    title = 'My Blog'
    # reverse lazy utility function is a lazily evaluated version of reverse
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my Blog'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self,item):
        return item.title
    
    # item is object 
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body),30)
    
    # item object defined in Post models
    def item_pubdate(self,item):
        return item.publish
