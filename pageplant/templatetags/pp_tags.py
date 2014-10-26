from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from django import template

from pageplant.models import Page

register = template.Library()


class RenderPartialPage(InclusionTag):
    template = 'pageplant/templatetags/render_partial_page.html'
    options = Options(
        Argument('slug')
    )

    def get_context(self, context, slug):
        try:
            page = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            page = '<div class="error">Mangler side: %s</div>' % slug

        return {'page': page}

register.tag(RenderPartialPage)
