# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from models import Job, Category, Comments, Likes


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        request = self.client.get('/')
        self.assertContains(request, text='Нет работ')

    def test_admin(self):
        request = self.client.get('/admin/')
        self.assertContains(request, text='Django')

class ModelsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="php",
                                      image="php.png")
        self.job = Job.objects.create(name="test",
                                      desc="description",
                                      category=self.category)
        self.comment = Comments.objects.create(text="lol",
                                              job=self.job)
        self.like = Likes.objects.create(job=self.job,
                                         type="1")

    def test_job(self):
        job = Job.objects.filter(name="test").get()
        self.assertEqual(job.__unicode__(), 'test')

    def test_category(self):
        cat = Category.objects.filter(name="php").get()
        self.assertEqual(cat.__unicode__(), 'php')

    def test_comment(self):
        comm = Comments.objects.filter(text="lol").get()
        self.assertEqual(comm.__unicode__(), 'lol/test')

    def test_like(self):
        like = Likes.objects.filter(job=self.job).get()
        self.assertEqual(like.__unicode__(), 'test/True')
