# -*- coding: utf-8 -*-
from decorators import render_json, render_to
from lulz.forms import AddJob, AddComment, SearchForm
from models import Job, Comments, Category, Likes
from django.core.mail import send_mail


escape = lambda string: string.replace("&", "&amp;").\
                               replace("<", "&lt;").\
                               replace(">", "&gt;").\
                               replace("\n", "<br>")


@render_to("jobs.html")
def home(request):
    """
    Home page

    @param request:
    @return json:
    """
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
    """
    Fetch vacanciec with catecory

    @param request:
    @return json:
    """
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
                                   "category": job.category.id,
                                   "desc": escape(job.desc),
                                   "likes": job.likes,
                                   "date": job.date.__str__(),
                                   "comments": job.jobcomm.count()})

        result["success"] = True
    return result


@render_json
def addvacancy(request):
    """
    Add vacancy

    @param request:
    @return json:
    """
    result = {"success": False}
    if request.POST:
        form = AddJob(request.POST)
        if form.is_valid():
            form.save()
            send_mail("Added new cavancy: %s" % form.cleaned_data["name"],
                       "Added new vacancy: %s" % form.cleaned_data["name"],
                       "report@joblulz.tk",
                       ["d1fffuz0r@gmail.com"])
            return {"success": True}
        else:
            return result
    else:
        return result


@render_json
def addcomment(request):
    """
    Create comment for vacancy

    @param request:
    @return json:
    """
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
    """
    Get full description for vacancy

    @param request:
    @return json:
    """
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
    """
    Like or Dislike vacancy

    @param request:
    @return json:
    """
    result = {"success": False}

    if request.POST:
        id = int(request.POST["id"])
        type = request.POST["type"]

        j = Job.objects.filter(pk=id)

        if j and j.get():
            job = j.get()
            like = Likes.objects.filter(job=job,
                                        agent=request.META["HTTP_USER_AGENT"],
                                        ip=request.META["REMOTE_ADDR"])
            if like:
                result.update({"message": "Уже голосовали"})
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
            return result
        else:
            return result
    return result
