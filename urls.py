"""
Definition of urls for djangotest.
"""

from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', djangotest.views.home, name='home'),
    # url(r'^djangotest/', include('djangotest.djangotest.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
	url(r'^$', include('posts.urls')),
    url(r'^posts/', include('posts.urls')),
	url(r'^register/', include('posts.urls')),
	url(r'^search/', include('search.urls')),
]