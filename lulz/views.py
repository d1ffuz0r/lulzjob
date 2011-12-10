# -*- coding: utf-8 -*-
from decorators import render_json, render_to
from lulz.forms import AddJob, AddComment, SearchForm
from models import Job, Comments, Category, Likes


escape = lambda string: string.replace("&", "&amp;").\
                               replace("<", "&lt;").\
                               replace(">", "&gt;")


@render_to("jobs.html")
def home(request):
    count = Job.objects.filter(published=True).count()
    jobs = Job.objects.filter(published=True).order_by("-id").all()
    categories = Category.objects.all()

    return {"count": count,
            "jobs": jobs,
            "categories": categories,
            "addjob": AddJob,
            "addcomment": AddComment,
            "search": SearchForm}


@render_json
def fetch(request):
    result = {"success": False, "jobs": []}

    if request.POST and request.POST["cat"]:
        id = int(request.POST["cat"])

        if id == 900009:
            jobs_pre = Job.objects.filter(
                published=True
            ).order_by("-id").all()
        else:
            jobs_pre = Job.objects.filter(
                published=True,
                category__id=id
            ).order_by("-id").all()

        for job in jobs_pre:
            result["jobs"].append({"id": job.id,
                                   "name": job.name,
                                   "desc": escape(job.desc),
                                   "tags": job.tags,
                                   "likes": job.likes,
                                   "link": job.link,
                                   "date": job.date.__str__(),
                                   "comments": job.jobcomm.count(),
                                   "category": job.category.id})

        result["success"] = True
    return result


@render_json
def addvacancy(request):
    result = {"success": False}
    if request.POST:
        form = AddJob(request.POST)
        if form.is_valid():
            form.save()
            return {"success": True}
        else:
            return result
    else:
        return result


@render_json
def addcomment(request):
    result = {"success": False}
    if request.POST:
        form = AddComment(request.POST)
        if form.is_valid():

            f = form.save(commit=False)
            f.agent = request.META["HTTP_USER_AGENT"]
            f.ip = request.META["REMOTE_ADDR"]
            f.save()

            result["success"] = True
            result["text"] = request.POST["text"]

            return result
        else:
            return result
    else:
        return result


@render_json
def full(request):
    result = {"success": False}
    if request.POST:
        job = Job.objects.filter(published=True).\
            get(pk=int(request.POST["id"]))
        image = job.category.image.order_by("?")[0].image

        result["id"] = job.id
        result["link"] = job.link
        result["name"] = job.name
        result["desc"] = escape(job.desc)
        result["date"] = job.date.ctime()
        result["likes"] = job.likes
        result["cat_image"] = image.__str__()

        comments = []
        c = Comments.objects.filter(job=job).all()

        if c:
            for text in c:
                comments.append(escape(text.text))

        return {"success": True,
                "vacancy": result,
                "comments": comments}
    else:
        return result


@render_json
def like(request):
    result = {"success": False}
    if request.POST:
        id = int(request.POST["id"])
        type = request.POST["type"]

        job = Job.objects.filter(pk=id).get()

        if job:
            like = Likes.objects.filter(job=job,
                                        agent=request.META["HTTP_USER_AGENT"],
                                        ip=request.META["REMOTE_ADDR"])
            if like:
                result.update({"message": "Уже голосовали"})
                return result
            else:
                Likes.objects.create(job=job,
                                     type=type,
                                     agent=request.META["HTTP_USER_AGENT"],
                                     ip=request.META["REMOTE_ADDR"])
                if type == "like":
                    job.likes += 1
                    job.save()
                if type == "unlike":
                    job.likes -= 1
                    job.save()
                result.update({"success": True, "likes": job.likes})
        else:
            return result
    return result
