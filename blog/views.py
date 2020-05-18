from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreateForm, SignUpForm
from django.contrib.auth import login, authenticate

def home_view(request, *args, **kwargs):
	posts = Post.objects.all()
	context = {
		'posts': posts,
	}
	print(request.user)
	return render(request, "home.html", context)


def single_post_view(request, post_id):
	post = Post.objects.get(id=post_id)
	context = {
		'post': post,
	}

	return render(request, "post.html", context)


def create_post_view(request):
	if request.method == 'POST':
		form = PostCreateForm(request.POST, request.FILES)

	if form.is_valid():
		form.save()

	context = {
		'form': form,
	}

	return render(request, "new_post.html", context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def login_view(request):
	if request.method == 'POST' and request.user == 'AnonymousUser':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, 'account.html')
		else:
			print("invalid login")

	return render(request, 'login.html')