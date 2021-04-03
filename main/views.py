from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
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
    
    average1 = reviews.aggregate(Avg("design_rating"))["design_rating__avg"]
    average2 = reviews.aggregate(Avg("usability_rating"))["usability_rating__avg"]
    average3 = reviews.aggregate(Avg("content_rating"))["content_rating__avg"]

    average = average1 + average2 + average3

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


@login_required()
def add_projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:home")
    else:
        form = MovieForm()
    return render(request, 'main/addprojects.html', {'form': form, "controller":"Add Projects"}) 
