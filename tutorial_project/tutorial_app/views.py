from django.shortcuts import render
from models import Category, Page #this is our models.p
from forms import CategoryForm , PageForm, UserForm, UserProfileForm #forms is our forms.py
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponse


# Create your views here.
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
@login_required
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

@login_required
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

def register(request):
	registered = False
	if request.method == 'POST':
	# Attempt to grab information from the raw form information.
	# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			#Do*e wit* *serFor*
			#*ow T*e profile
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfilemodel.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				# Now we save the UserProfile model instance.
				profile.save()
				# Update our variable to tell the template registration was successful.
				registered = True
		else:

			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request,
			'register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
def user_login(request):
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('') as opposed to request.POST[''],
		# because the request.POST.get('') returns None, if the value does not exist,
		# while the request.POST[''] will raise key error exception
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		if user:
		# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/')
			else:
			# An inactive account was used - no logging in!
				return HttpResponse("Your account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect('/')