from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import ProfileForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer, ProfileSerializer

# Create your views here.


def home(request):
    query = request.GET.get('title')    
    
    allProjects = None
    if query:
        allProjects = Project.objects.filter(title__icontains=query)
    else:

        allProjects = Project.objects.all()
    context = {
        "projects": allProjects,
    }

    return render(request,'main/index.html', context)


def details(request, id):
    project = Project.objects.get(id=id)
    reviews = Review.objects.filter(project=id).order_by('-comment')
    
    average1 = reviews.aggregate(Avg("design_rating"))["design_rating__avg"]
    average2 = reviews.aggregate(Avg("usability_rating"))["usability_rating__avg"]
    average3 = reviews.aggregate(Avg("content_rating"))["content_rating__avg"]

    average = (average1 + average2 + average3) / 3

    if average == None:
        average = 0
    average = round(average, 2)

    context = {
        "project": project,
        "reviews": reviews,
        "average": average,

    }

    return render( request,'main/details.html', context)





# def details(request, id):
#     project = Project.objects.get(id=id)
#     ratings = Rating.objects.filter(user=request.user, project=project).first()
#     rating_status = None
#     if ratings is None:
#         rating_status = False
#     else:
#         rating_status = True
#     if request.method == 'POST':
#         form = RatingsForm(request.POST)
#         if form.is_valid():
#             rate = form.save(commit=False)
#             rate.user = request.user
#             rate.project = project
#             rate.save()
#             project_ratings = Rating.objects.filter(project=project)

#             design_ratings = [d.design for d in project_ratings]
#             design_average = sum(design_ratings) / len(design_ratings)

#             usability_ratings = [us.usability for us in project_ratings]
#             usability_average = sum(usability_ratings) / len(usability_ratings)

#             content_ratings = [content.content for content in project_ratings]
#             content_average = sum(content_ratings) / len(content_ratings)

#             score = (design_average + usability_average + content_average) / 3
#             print(score)
#             rate.design_average = round(design_average, 2)
#             rate.usability_average = round(usability_average, 2)
#             rate.content_average = round(content_average, 2)
#             rate.score = round(score, 2)
#             rate.save()
#             return HttpResponseRedirect(request.path_info)
#     else:
#         form = RatingsForm()
#     params = {
#         'project': project,
#         'rating_form': form,
#         'rating_status': rating_status

#     }
#     return render(request, 'main/details.html', params)



@login_required()
def add_projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST or None, request.FILES,)

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user.profile
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
            print(form.errors)
            print(form)
            if form.is_valid():
                data = form.save(commit=False)

            # rate_form = ReviewForm(request.POST)
            # if rate_form.is_valid():
            #     data = rate_form.save(commit=False)
                # data.comment = request.POST['comment']
                # data.design_rating = request.POST['design_rating']
                # data.usability_rating = request.POST['usability_rating']
                # data.content_rating = request.POST['content_rating']
                data.user = request.user.profile
                data.project = project
                data.save()
                return redirect("main:details", id)
        else:

            form = ReviewForm()
        return render(request, "main/details.html", {'form': form, "project":project})

        #     rate_form = ReviewForm()
        # return render(request, "main/details.html", {'rate_form': rate_form})

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
                    if (data.degin_rating > 10) or (data.design_rating < 0):
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


def userpage(request,):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid():
		    user_form.save()
		    messages.success(request,('Your profile was successfully updated!'))
		elif profile_form.is_valid():
		    profile_form.save()
		    messages.success(request,('Your Projects were successfully updated!'))
		else:
		    messages.error(request,('Unable to complete request'))
		# return redirect ("main:userpage")
	user_form = UserForm(instance=request.user)
	profile_form = ProfileForm(instance=request.user.profile)
	return render(request = request, template_name ="main/user.html", context = {"user":request.user, 
		"user_form": user_form, "profile_form": profile_form })



class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)