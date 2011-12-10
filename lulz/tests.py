# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import skip
from django.test.client import Client
from lulz.models import Image
from models import Job, Category, Comments, Likes


class ViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="php")
        self.client = Client()

    def test_home(self):
        request = self.client.get("/")
        self.assertContains(request, text="ДЖОПЛУЛЗ")

    def test_admin(self):
        request = self.client.get("/admin/")
        self.assertContains(request, text="Django")

    def test_full_vacancy_get_fail(self):
        request = self.client.get("/ajax/full/")
        self.assertEqual(request.content, '{"success": false}')

    def test_full_vacancy_ajax_true(self):
        self.image = Image.objects.create(name="phpp",
                                          image="img/php.png")

        category = Category.objects.create(name="php")
        category.image.add(self.image)
        self.job = Job.objects.create(name="test",
                                      desc="description",
                                      category=category,
                                      published=True)
        self.comment = Comments.objects.create(text="lol",
                                               job=self.job)
        request = self.client.post("/ajax/full/", data={
            "id": self.job.id
        })
        self.assertContains(request, "vacancy")

    def test_create_comment_get_false(self):
        request = self.client.get("/ajax/addcomment/")
        self.assertEqual(request.content, '{"success": false}')

    @skip("working")
    def test_create_comment_ajax_true(self):
        self.image = Image.objects.create(name="phpp",
                                          image="img/php.png")
        category = Category.objects.create(name="php", image=[1])
        Job.objects.create(name="test",
                           desc="description",
                           category=category)
        print self.job.id
        request = self.client.post("/ajax/addcomment/", data={
            "text": "test",
            "job": 1
        })
        self.assertEqual(request.content, '{"success": true}')

    def test_create_comment_ajax_false(self):
        request = self.client.post("/ajax/addcomment/", data={
            "text": "test"
        })
        self.assertEqual(request.content, '{"success": false}')

    def test_create_vacancy_get_false(self):
        request = self.client.get("/ajax/addvacancy/")
        self.assertEqual(request.content, '{"success": false}')

    def test_create_vacancy_ajax_true(self):
        request = self.client.post("/ajax/addvacancy/", data={
            "name": "test",
            "desc": "testdesc",
            "tags": "test, test1, test2",
            "category": 1,
            "link": "http://google.com"
        })
        self.assertEqual(request.content, '{"success": true}')

    def test_create_vacancy_ajax_false(self):
        request = self.client.post("/ajax/addvacancy/", data={
            "name": "test",
            "desc": "testdesc",
            "tags": "test, test1, test2",
            "category": 1,
        })
        self.assertEqual(request.content, '{"success": false}')


class ModelsTest(TestCase):
    def setUp(self):
        self.image = Image.objects.create(name="phpp",
                                          image="img/php.png")

        self.category = Category.objects.create(name="php")

        self.job = Job.objects.create(name="test",
                                      desc="description",
                                      category=self.category)

        self.comment = Comments.objects.create(text="lol",
                                               job=self.job)

        self.like = Likes.objects.create(job=self.job,
                                         type="1")

    def test_job(self):
        job = Job.objects.filter(name="test").get()
        self.assertEqual(job.__unicode__(), "test")

    def test_category(self):
        cat = Category.objects.filter(name="php").get()
        self.assertEqual(cat.__unicode__(), "php")

    def test_comment(self):
        comm = Comments.objects.filter(text="lol").get()
        self.assertEqual(comm.__unicode__(), "lol/test")

    def test_like(self):
        like = Likes.objects.filter(job=self.job).get()
        self.assertEqual(like.__unicode__(), "test/True")

    def test_image(self):
        image = Image.objects.filter(name="phpp").get()
        self.assertEqual(image.__unicode__(), "phpp")
