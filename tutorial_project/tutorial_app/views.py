from django.shortcuts import render
from models import Category, Page #this is our models.p
from forms import CategoryForm , PageForm #forms is our forms.py



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
		print 'sorry ' + str(category_name_slug) + ' does not exist'
	return render(request, 'category.html', context_dict)
def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST) #validate input with CategoryForm class
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
		return render(request, 'add_category.html', {'form':form})
def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
			else:
				print form.errors
		else:
			print form.errors
	else:
		form = PageForm()
		context_dict = {'form':form, 'category': cat, 'slug': category_name_slug}
		return render(request, 'add_page.html', context_dict)


