from decorators import render_json
from forms import AddJob
from models import Job

@render_json
def addvacancy(request):
    form = AddJob(request.POST)
    if form.is_valid():
        form.save()
        return {"success": True}
    else:
        return {"success": False}


@render_json
def full(request):
    result = {}
    if request.POST:
        job = Job.objects.filter(published=True).get(pk=request.POST["id"])
        result['name'] = job.name
        result['desc'] = job.desc
        result['cat_image'] = job.category.image.__str__()

        return {"success": True, "vacancy": result}
    else:
        return {"success": False}