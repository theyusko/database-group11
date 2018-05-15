from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
	url(r'^process_query', views.process_query, name="process_query"),
]