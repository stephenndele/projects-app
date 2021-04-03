from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
# Create your views here.


def home(request):
    query = request.GET.get('title')
    allProjects = None
    if query:
        allProjects = Project.objects.filter(name__icontains=query)
    else:

        allProjects = Project.objects.all()
    context = {
        "projects": allProjects,
    }

    return render( request,'main/index.html', context)


def details(request, id):
    project = Project.objects.get(id=id)
    reviews = Review.objects.filter(movie=id).order_by('-comment')
    
    average = reviews.aggregate(Avg("design_rating"))["design_rating__avg"]
    # "usability_rating" , "content_rating"))
    # ["design_rating__avg", "content_rating__avg", "content_rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)

    context = {
        "Project": project,
        "reviews": reviews,
        "average": average,

    }

    return render( request,'main/details.html', context)