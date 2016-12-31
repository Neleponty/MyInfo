"""MyInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from standartRouteHandler import Handler
"""from standartRouteHandler import parser_e1
parser_e1.ParserE1().start(100)"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'news/', Handler.GetNews.as_view()),
    url(r'^categories/categoryId=(?P<categoryId>\d*)', Handler.GetNewsToCategory.as_view()),
    url(r'^categories/', Handler.CategoriesApi.as_view()),
    url(r'^news/location/newsId=(?P<newsId>\d*)', Handler.GetLocationsToNews.as_view()),
    url(r'^opinions/location/opinionId=(?P<opinionId>\d*)', Handler.GetLocationsToOpinions.as_view()),
    url(r'^opinions/opinionId=(?P<opinionId>\d*)', Handler.GetPhotosToOpinions.as_view()),
    url(r'^photos/newsId=(?P<newsId>\d*)', Handler.PhotosToNews.as_view()),
    url(r'^album/', Handler.GetAlbum.as_view()),
    url(r'^album/photos/albumId=(?P<albumId>\d*)', Handler.ImagesForAlbum.as_view())
]
