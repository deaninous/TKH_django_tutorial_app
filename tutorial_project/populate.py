import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial_project.settings')
import django
django.setup()
from tutorial_app.models import Category, Page

def add_cat(name):
	c = Category.objects.get_or_create(name=name)[0]
	return c
def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title = title)[0]
	p.url = url
	p.views = views
	p.save()
	return p
def populate():
	python_cat = add_cat('Python')
	add_page(cat = python_cat,
		title = 'Official Python Mooch',
		url='http://docs.house.org/mooch')
	add_page(cat = python_cat,
		title = "How to loose it within 10 days",
		url = "http://lost.position.vandal.out")
	add_page(cat = python_cat,
		title = "loose 10 millions",
		url = "http://sell.forget.regret.aww")
	django_cat = add_cat("Django")
	add_page(cat = django_cat,
		title = 'Django Unchained',
		url = 'http://jamy.fox.mil'
		)
	add_page(cat = django_cat,
		title = 'Djungle boy',
		url = 'http://jungle.mogly.woo'
		)
	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print "-{0} - {1}".format(str(c), str(p))

if __name__ == '__main__':
	print "Starting Django population script..."
	populate()
