"""twittermap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from twitmap import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/(?P<keyword>[A_Za-z0-9\s]*)$', views.search_by_keyword, name='search_by_keyword'),
    url(r'^scroll/(?P<sid>[\d\w]*)', views.scroll_results, name='scroll_results'),
    url(r'^test_search/(?P<keyword>[A_Za-z0-9\s]*)$', views.test_search, name='test_search'),
    url(r'^process_tweet/', views.process_tweet),
    url(r'^sse/$', views.SseEndpoint.as_view(), name='sse_endpoint'),
    url(r'^', include('twitmap.urls'))
]
