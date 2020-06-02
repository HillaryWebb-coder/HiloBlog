from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreateForm, SignUpForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

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


# def create_post_view(request):
# 	if request.method == 'POST':
# 		form = PostCreateForm(request.POST, request.FILES)

# 	if form.is_valid():
# 		form.save()

# 	context = {
# 		'form': form,
# 	}

# 	return render(request, "new_post.html", context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login', permanent=True)
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def login_view(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = AuthenticationForm(request.POST)
			#print(request.POST['username'])
			user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
			if user is not None:
				login(request, user)
				return redirect('account', permanent=True)
		else:
			form = AuthenticationForm()
		

		return render(request, 'login.html', {'form':form})

	else:
		return redirect('account', permanent=True)
		


def account_view(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			post_form = PostCreateForm(request.POST, request.FILES)
			profileform = ProfileForm(request.POST, request.FILES)

			if form.is_valid():
				form.save()
		else:
			post_form = PostCreateForm()
			profileform = ProfileForm()
		
		return render(request, 'account.html', {'post_form': post_form, 'profileform': profileform})
	else:
		return redirect('login', permanent=True)
	

def profile_view(request):
	user_profile = request.user.profile
	return render(request, 'profile.html', {'user_profile': user_profile})


def logout_view(request):
	logout(request)
	return redirect('home')