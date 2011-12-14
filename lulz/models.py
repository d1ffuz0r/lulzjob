# -*- coding: utf-8 -*-
from django.db import models


class Image(models.Model):
    """
    Image model

    @param name: str
    @param image: file object
    """
    name = models.CharField(max_length=100,
                            verbose_name=u"Название")
    image = models.ImageField(upload_to="backgrounds",
                                  verbose_name=u"Фон")

    class Meta:
        verbose_name = u"Изображение"
        verbose_name_plural = u"Изображения"

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
    Category

    @param name: str
    @param image: file object
    """
    name = models.CharField(max_length=100,
                            blank=False,
                            verbose_name=u"Название")
    image = models.ManyToManyField(Image,
                                   related_name="catimages",
                                   verbose_name=u"Фон")

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"

    def __unicode__(self):
        return self.name


class Job(models.Model):
    """
    Job model

    @param name: str
    @param desc: str
    @param tags: str
    @param likes: int
    @param link: url
    @param published: boolean
    @param date: datetime
    @param category: foreignkey Category
    @param comments: ManyToManyField Comments
    """
    name = models.CharField(max_length=100,
                            verbose_name=u"Заголовок")
    desc = models.TextField(max_length=1000,
                            verbose_name=u"Комментарий")
    tags = models.CharField(max_length=100,
                            verbose_name=u"Теги")
    likes = models.IntegerField(verbose_name=u"Лайки", default=0)
    link = models.URLField(max_length=100,
                           verbose_name=u"Ссылка на оригинал")
    published = models.BooleanField(default=False,
                                    verbose_name=u"Опубликовано")
    date = models.DateTimeField(auto_now=True,
                                verbose_name=u"Дата публикации")
    category = models.ForeignKey(Category,
                                 verbose_name=u"Категория")
    comments = models.ManyToManyField("Comments",
                                      related_name="jobcomm",
                                      blank=True,
                                      verbose_name=u"Комментарии")

    class Meta:
        verbose_name = u"Вакансия"
        verbose_name_plural = u"Вакансии"

    def __unicode__(self):
        return self.name


class Comments(models.Model):
    """
    Comments model

    @param text: str
    @param job: foreignkey Job
    @param agent: str
    @param ip: str
    """
    text = models.CharField(max_length=200,
                            verbose_name=u"Текст комментария")
    job = models.ForeignKey(Job,
                            related_name="jobcomm",
                            verbose_name=u"Вакансия")
    agent = models.CharField(max_length=200, verbose_name=u"User-Agent")
    ip = models.CharField(max_length=100, verbose_name=u"IP")

    class Meta:
        verbose_name = u"Комментарий"
        verbose_name_plural = u"Комментарии"

    def __unicode__(self):
        return "%s/%s" % (self.text[:10], self.job.name)


class Likes(models.Model):
    """
    Likes model

    @param job: foreignkey Job
    @param agent: str
    @param ip: str
    """
    CHOISES = (
        ("1", "+"),
        ("0", "-")
    )
    job = models.ForeignKey(Job,
                            related_name="joblikes",
                            verbose_name=u"Вакансия")
    agent = models.CharField(max_length=200, verbose_name=u"User-Agent")
    ip = models.CharField(max_length=100, verbose_name=u"IP")
    type = models.BooleanField(choices=CHOISES, verbose_name=u"Тип")

    class Meta:
        verbose_name = u"Лайк"
        verbose_name_plural = u"Лайки"

    def __unicode__(self):
        return "%s/%s" % (self.job.name, self.type)
