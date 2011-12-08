from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView
from lulz.models import Job
from lulz.views import addvacancy, full
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Job.objects.filter(published=True).all()[:10],
                                     context_object_name="jobs",
                                     template_name="jobs.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/addvacancy/$', addvacancy),
    url(r'^ajax/full/$', full),
    url(r"^media/(?P<path>.*)$",
            "django.views.static.serve",
                {"document_root": settings.MEDIA_ROOT}),
        url(r"^static/(?P<path>.*)$",
            "django.views.static.serve",
                {"document_root": settings.STATIC_ROOT}),
)
