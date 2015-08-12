from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import app1.urls
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include(app1.urls)),
)
