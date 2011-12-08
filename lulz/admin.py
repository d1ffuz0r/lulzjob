from django.contrib import admin
from django.contrib.auth.models import Group
from models import Category, Comments, Job, Likes


class AdminJobs(admin.ModelAdmin):
    list_display = ("name", "date", "published")


class AdminCategory(admin.ModelAdmin):
    list_display = ("name",)


class AdminComments(admin.ModelAdmin):
    list_display = ("text", "job")

class AdminLikes(admin.ModelAdmin):
    list_display = ("ip", "type")

admin.site.register(Category, AdminCategory)
admin.site.register(Comments, AdminComments)
admin.site.register(Job, AdminJobs)
admin.site.register(Likes, AdminLikes)
admin.site.unregister(Group)