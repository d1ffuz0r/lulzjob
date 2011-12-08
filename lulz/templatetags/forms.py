from django import template
from lulz.forms import AddJob, AddComment, SearchForm
register = template.Library()


@register.simple_tag()
def addjob():
    return AddJob()


@register.simple_tag()
def addcomment():
    return AddComment().as_p()


@register.simple_tag()
def search():
    return SearchForm()