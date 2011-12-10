from django.contrib import admin
from django.contrib.auth.models import Group
from models import Category, Comments, Job, Likes, Image


class AdminImages(admin.ModelAdmin):
    list_display = ("name", "image",)


class AdminJobs(admin.ModelAdmin):
    list_display = ("name", "category", "published", "date")


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
