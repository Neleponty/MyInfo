# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Attractions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    coord = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attractions'




class Categories(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'categories'


class CategoriesLinks(models.Model):
    parent_id = models.IntegerField()
    child_id = models.IntegerField()
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'categories_links'


class LocationNewsEvent(models.Model):
    id = models.AutoField(primary_key=True)
    news = models.ForeignKey('News', models.DO_NOTHING)
    coord = models.TextField()

    class Meta:
        managed = False
        db_table = 'location_news_event'


class PhotosUrls(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=300)

    def setPath(self,id,path):
        self.id = id
        self.path = path
        return self

    class Meta:
        managed = False
        db_table = 'photos_urls'

class News(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField()
    name = models.CharField(max_length=2000)
    header = models.CharField(max_length=2000)
    content = models.TextField()
    category = models.ForeignKey(Categories, models.DO_NOTHING, db_column='id_categ')
    is_fav = models.BooleanField()
    likes = models.IntegerField()
    image = models.ForeignKey('PhotosUrls', models.DO_NOTHING, null=True)
    scale = models.IntegerField(blank=True, null=True)
    photos = models.ManyToManyField(PhotosUrls,
                                    through='NewsPhotos',
                                    through_fields=('photo', 'news'))

    class Meta:
        managed = False
        db_table = 'news'


class NewsPhotos(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ForeignKey('PhotosUrls', models.DO_NOTHING)
    news = models.ForeignKey('News', models.DO_NOTHING)

    def setPhoto(self, id, photo, news):
        self.id = id
        self.news = news
        self.photo = photo
        return self
    class Meta:
        managed = False
        db_table = 'news_photos'


class Opinions(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField()
    title = models.TextField()
    headline = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(PhotosUrls,
                                    through='OpinionsImages',
                                    through_fields=('photo', 'opinion'))


    class Meta:
        managed = False
        db_table = 'opinions'


class OpinionsImages(models.Model):
    id = models.AutoField(primary_key=True)
    opinion = models.ForeignKey('Opinions', models.DO_NOTHING)
    photo = models.ForeignKey('PhotosUrls', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'opinions_images'


class OpinionsLocations(models.Model):
    id = models.AutoField(primary_key=True)
    opinion_id = models.IntegerField()
    coord = models.TextField()

    class Meta:
        managed = False
        db_table = 'opinions_locations'


class OpinionsToTags(models.Model):
    id = models.AutoField(primary_key=True)
    opinions = models.ForeignKey(Opinions, models.DO_NOTHING)
    tags = models.ForeignKey('Tags', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'opinionstotags'


class PhotoAlbumsTitle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    title_image = models.ForeignKey('PhotosUrls', models.DO_NOTHING, db_column='title_image', blank=True, null=True)
    photos = models.ManyToManyField(PhotosUrls,
                                    through='PhotosInAlbums',
                                    through_fields=('photo', 'album'))

    class Meta:
        managed = False
        db_table = 'photoalbums_title'


class PhotosInAlbums(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey('PhotoAlbumsTitle', models.DO_NOTHING)
    photo = models.ForeignKey('PhotosUrls', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'photos_in_albums'


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'tags'


class TourPoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    coordinates = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(PhotosUrls, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tour_point'


class Tours(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tours'


class ToursToPoints(models.Model):
    id = models.AutoField(primary_key=True)
    tours = models.ForeignKey(Tours, models.DO_NOTHING)
    point = models.ForeignKey(TourPoint, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tours_to_points'


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.TextField()
    name = models.TextField(blank=True, null=True)
    hashpass = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'


