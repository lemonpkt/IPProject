from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
	
	url(r'^freeAgent/',include('freeAgent.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
