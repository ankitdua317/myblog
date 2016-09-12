from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

def post_create(request): #is a function
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_detail(request ,id=None): #is a function
	instance = get_object_or_404(Post, id=id)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)	
	context = {
	"z" : instance,
	"title" : instance.title,
	"share_string" : share_string
	}
	return render(request,"details.html",context)

def post_list(request): 
	today = timezone.now().date()
	queryset_list = Post.objects.active().order_by("-publish")#,"-timestamp","-updated") 
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all().order_by("-publish")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()	
	paginator = Paginator(queryset_list, 2) #shows 10 posts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
	"title" : "List",
	"list" : queryset,
	"page_var" : page_var,
	"today" : today,
	}
	return render(request,"post_list.html",context)
	#return HttpResponse("<h1>Fuck Off Nihal</h1>")

def post_update(request, id=None): #is a function
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Item Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title" : "Update",
		"instance":instance,
		"form":form,
	}
	return render(request,"post_form.html",context)

def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	return redirect("posts:list")
	#context = {
	#"title" : "Delete"
	#}
	#return render(request,"index1.html",context)