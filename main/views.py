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