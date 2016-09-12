from django.shortcuts import render
from .models import Match

# Create your views here.
def home(request):
	x = 23
	y = Match.objects.all()
	context = {"pappu":x, "objects":y}
	return render(request,"index.html",context)

def scorepage(request):
	return render(request,"score1.html",{})