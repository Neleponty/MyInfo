from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.serializers import HyperlinkedModelSerializer
from MyInfo.standartRouteHandler import SimpleModel
from django.core import serializers


class AttractionsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.Attractions
        fields = ('id', 'name', 'coord', 'description', 'image')


class NewsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.News
        fields = ('id', 'pub_date', 'header', 'content', 'likes', 'is_fav')

1
class GetNewsToCategory(APIView):
    def get(self, request, categoryId):
        query = SimpleModel.News.objects.get(category=categoryId)
        return Response(NewsSerializer(query).data)


class OpinionsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.News
        fields = ('id', 'pub_date', 'title', 'headline', 'image', 'text')

2
class GetOpinions(APIView):
    def get(self, request):
        query = SimpleModel.Opinions.objects.all()
        return Response(OpinionsSerializer(query).data)


class PhotosSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.PhotosUrls
        fields = ('id', 'path')

3
class GetPhotosToOpinions(APIView):
    def get(self, request, opinionId):
        query = SimpleModel.PhotosUrls.objects.filter(opinions__id=opinionId)
        return Response(PhotosSerializer(query).data)

4

# Отдать фото для новости
class PhotosToNews(APIView):
    def get(self, request, newsId):
        query = SimpleModel.News.objects.get(id=newsId) \
            .photos__set.all()
        return Response(PhotosSerializer(query).data)


def fromQuery(query):
    coords = []
    for item in query:
        coords.append(item.coord)
    serialized = serializers.serialize('json', coords)
    return HttpResponse(serialized)

5

class GetLocationsToNews(APIView):
    def get(self, request, newsId):
        query = SimpleModel.LocationNewsEvent.objects. \
            filter(news=newsId)
        return fromQuery(query)

6
class GetLocationsToOpinions(APIView):
    def get(self, request, opinionId):
        query = SimpleModel.OpinionsLocations.objects. \
            filter(opinion_id=opinionId)
        return fromQuery(query)


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.Categories
        fields = ('id', 'name')


class AlbumSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SimpleModel.PhotoAlbumsTitle
        fields = ('id', 'name', 'description','title_image')


class GetAlbum(APIView):
    def get(self, request):
        album = SimpleModel.PhotoAlbumsTitle.objects.all()
        return Response(AlbumSerializer(album).data)


class ImagesForAlbum(APIView):
    def get(self, albumId, request):
        query = SimpleModel.PhotoAlbumsTitle.objects.get(id=albumId)
        return Response(PhotosSerializer(query.photos).data)

/30
5''0.23


7
# Вопрос, как отдавать
class CategoriesApi(APIView):
    def get(self, request):
        query = SimpleModel.Categories.objects.all()

        return Response(CategorySerializer(data=query).data)

    def put(self, request):
        dataToValid = CategorySerializer(request.data)
        if dataToValid.is_valid():
            dataToValid.save()
            return Response(dataToValid.data, status=status.HTTP_200_OK)
        else:
            return Response('', status=status.HTTP_400_BAD_REQUEST)


