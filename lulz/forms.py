# -*- coding: utf-8 -*-
from django import forms
from lulz.models import Job, Comments, Category


class AddJob(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("name", "desc", "tags", "link", "category")
        widgets = {
            "name": forms.TextInput(attrs={"class": "required"}),
            "desc": forms.Textarea(attrs={"class": "required"}),
            "tags": forms.TextInput(attrs={"class": "required"}),
            "link": forms.TextInput(attrs={"class": "required url"}),
            "cateogry": forms.CheckboxInput(attrs={"class": "required digits"}),
        }


class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("text",)


class SearchForm(forms.Form):
    query = forms.CharField(label=u'Ключевое слово')
    cat = forms.IntegerField(
        label=u'Категория',
        widget=forms.Select(
            choices=Category.objects.all().values_list('id', 'name')
        )
    )
