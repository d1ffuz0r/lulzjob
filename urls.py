from django.conf.urls.defaults import patterns, include, url
from lulz.views import home, addvacancy, full, addcomment, fetch, like
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/addvacancy/$', addvacancy),
    url(r'^ajax/addcomment/$', addcomment),
    url(r'^ajax/full/$', full),
    url(r'^ajax/fetch/$', fetch),
    url(r'^ajax/like/$', like),
    url(r"^site_media/(?P<path>.*)$",
            "django.views.static.serve",
                {"document_root": settings.MEDIA_ROOT}),
        url(r"^static/(?P<path>.*)$",
            "django.views.static.serve",
                {"document_root": settings.STATIC_ROOT}),
)
