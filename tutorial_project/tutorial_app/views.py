from django.shortcuts import render
from models import Category, Page #this is our models.p

# Create your views here.
from django.http import HttpResponse
def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories' : category_list, 'pages' : page_list }
	return render(request, 'index.html', context_dict)
def about(request):
	return HttpResponse('about')
def category(request, category_name_slug):
	try:

		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'category.html', context_dict)