from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about_me(request):
	return render(request, 'about.html')

def post(request):
	return render(request, 'blog-post.html')