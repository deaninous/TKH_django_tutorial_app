from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
	context_dict = {'boldmessage':'tuturial here!'}
	return render(request, 'index.html', context_dict)
def about(request):
	return HttpResponse('about')