# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from models import Category, Comments, Job, Likes, Image


class AdminImages(admin.ModelAdmin):
    list_display = ("name", "image",)


class AdminJobs(admin.ModelAdmin):
    list_display = ("name", "category", "published", "date")
    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        """
        Show selected vacancies
        @param request:
        @param queryset: Selected vacancy
        @return:
        """
        public = queryset.update(published=True)
        if public == 1:
            message_bit = u"1 вакансия была опубликована"
        else:
            message_bit = u"%s вакансии были опубликованы" % rows_updated
        self.message_user(request, "%s" % message_bit)
    publish.short_description = u"Опубликовать выбраные Вакансии"

    def unpublish(self, request, queryset):
        """
        Hide selected vacancies
        @param request:
        @param queryset: Selected vacancy
        @return:
        """
        ubpub = queryset.update(published=False)
        if ubpub == 1:
            message_bit = u"1 вакансия был убрана"
        else:
            message_bit = u"%s вакансии были убраны" % rows_updated
        self.message_user(request, "%s из опубликованых" % message_bit)
    unpublish.short_description = u"Убрать из опубликованых"


class AdminCategory(admin.ModelAdmin):
    list_display = ("name",)


class AdminComments(admin.ModelAdmin):
    list_display = ("text", "job", "ip", "agent")


class AdminLikes(admin.ModelAdmin):
    list_display = ("ip", "type")


admin.site.register(Image, AdminImages)
admin.site.register(Category, AdminCategory)
admin.site.register(Comments, AdminComments)
admin.site.register(Job, AdminJobs)
admin.site.register(Likes, AdminLikes)
admin.site.unregister(Group)
