from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import ProfileForm, UserForm
from django.contrib.auth.forms import UserCreationForm

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

    return render(request,'main/index.html', context)


def details(request, id):
    project = Project.objects.get(id=id)
    reviews = Review.objects.filter(project=id).order_by('-comment')
    
    # average1 = reviews.aggregate(Avg("design_rating"))["design_rating__avg"]
    # average2 = reviews.aggregate(Avg("usability_rating"))["usability_rating__avg"]
    # average3 = reviews.aggregate(Avg("content_rating"))["content_rating__avg"]

    # average = average1 + average2 + average3

    # "usability_rating" , "content_rating"))
    # ["design_rating__avg", "content_rating__avg", "content_rating__avg"]
    average = reviews.aggregate(Avg("design_rating"))["design_rating__avg"]

    if average == None:
        average = 0
    average = round(average, 2)

    context = {
        "project": project,
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
            # data.user = request.user.project
            data.save()
            return redirect("main:home")
    else:
        form = ProjectForm()
    return render(request, 'main/addprojects.html', {'form': form, "controller":"Add Projects"}) 





@login_required()
def edit_projects(request, id):
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=project)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:details", id)
    else:
        form = ProjectForm(instance=project)
    return render(request,'main/addprojects.html', {"form": form, "controller":"Edit Project"})

@login_required()
def delete_projects(request, id):

    project = Project.objects.get(id=id)
    project.delete()
    return redirect("main:home")

@login_required()
def add_review(request, id):
    if request.user.is_authenticated:
        project = Project.objects.get(id=id)
        if request.method == 'POST':
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.design_rating = request.POST['design_rating']
                data.usability_rating = request.POST['usability_rating']
                data.content_rating = request.POST['content_rating']
                data.user = request.user
                data.project = project
                data.save()
                return redirect("main:details", id)
        else:
            form = ReviewForm()
        return render(request, "main/details.html", {'form': form})
    else:
        return redirect("accounts:login")

def edit_review(request, project_id, review_id):
    if request.user.is_authenticated:
        project = Project.objects.get(id=project_id)

        review = Review.objects.get(project=project, id=review_id)

        # check id user is logged in is the one who did review
        if request.user == review.user:
            # give permissions
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "out of allowed range, must be between 0 and 10."
                        return render(request, 'main/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:details", project_id)
            else:
                form = ReviewForm(instance= review)
            return render(request, "main/editreview.html", {'form': form})
        else:
            return redirect('main:details', project_id)
    else:
        return redirect("accounts:login")


@login_required()
def delete_review(request, project_id, review_id):
    if request.user.is_authenticated:
        projects = Project.objects.get(id=project_id)

        review = Review.objects.get(project=project, id=review_id)

        # check id user is logged in is the one who did review
        if request.user == review.user:
            review.delete()

        return redirect('main:details', project_id)
            
    else:
        return redirect("accounts:login")


def userpage(request):
	user_form = UserCreationForm(instance=request.user)
	profile_form = ProfileForm(instance=request.user.profile)
	return render(request=request, template_name="main/user.html", context={"user":request.user, "user_form":user_form, "profile_form":profile_form })




