from django import template

from ..models import Post

register = template.Library()


@register.inclusion_tag('papermill/templatetags/latest_posts_overview.html',
                        takes_context=True)
def latest_posts_overview(context, show_lead=True):
    """
    Renders latest posts overview
    """

    posts = Post.latest.posts(count=50)

    return {
        'posts': posts,
        'show_lead': show_lead,
    }
