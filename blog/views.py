from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Comment
from .forms import PostCreateForm, SignUpForm, CommentForm
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count

def post_list_view(request, *args, **kwargs):
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 2)
	page = request.GET.get('page')
	tags = Post.tags.all()

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {
		'page': page,
		'posts': posts,
		'tags': tags
	}
	print(request.user)
	return render(request, "home.html", context)


def single_post_view(request, year, month, day, post):
	post	=	get_object_or_404(Post,	slug=post, 
										status='published',	
										publish__year=year,	
										publish__month=month, 
										publish__day=day)

	comments = post.comments.filter(active=True)

	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()


	tags = Post.tags.all()

	post_tags_ids	=	post.tags.values_list('id',	flat=True) 
	similar_posts	=	Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) 
	similar_posts	=	similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form,
		'tags': tags,
		'similar_posts': similar_posts
	}

	return render(request, "post.html", context)


def post_list_by_tag_view(request, tag_slug=None):
	post_list = Post.objects.all()
	tags = Post.tags.all()

	tag	= None	
	
	if	tag_slug:									
		tag	=	get_object_or_404(Tag,	slug=tag_slug)									
		post_list	= post_list.filter(tags__in=[tag])


	paginator = Paginator(post_list, 2)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {
		'page': page,
		'posts': posts,
		'tag': tag,
		'tags': tags
	}
	print(request.user)
	return render(request, "post_tags_list.html", context)


# def create_post_view(request):
# 	if request.method == 'POST':
# 		form = PostCreateForm(request.POST, request.FILES)
#
# 	if form.is_valid():
# 		form.save()
#
# 	context = {
# 		'form': form,
# 	}
#
# 	return render(request, "new_post.html", context)

#
# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('')
#     else:
#         form = SignUpForm()
#
#     return render(request, 'signup.html', {'form': form})


#
# def login_view(request):
# 	if not request.user.is_authenticated:
# 		if request.method == 'POST' and request.user == 'AnonymousUser':
# 			username = request.POST['username']
# 			password = request.POST['password']
#
# 			user = authenticate(request, username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				return render(request, 'account.html')
# 			else:
# 				print("invalid login")
#
# 	else:
# 		return render(request, "account.html")
#
# 	return render(request, 'login.html')