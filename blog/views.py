from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


def search_post(request):
    posts = []
    query = None
    if request.method == 'POST':
        query = request.POST['query']
        posts = Post.published.annotate(
            search=SearchVector('title', 'body')
        ).filter(search=query)
    print(posts)
        
    return render(request, 'blog/search.html', {'posts':posts, 'query':query})



def recent_post(request):
    posts = Post.objects.all()[:2]
    tags = Tag.objects.all()
    
    most_commented_posts = Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:4]
    
    return render(request, 'blog/recent_post.html', 
                  {'posts':posts, 'tags':tags, 
                   'most_commented_posts':most_commented_posts})


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']
        comment = Comment(name=name, email=email, body=body)
        comment.post = post
        comment.save()
        return redirect(post.get_absolute_url())
    
    return redirect('post_comment')


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f' {cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n{cd["name"]}\' comments: {cd["comments"]}'
            
            send_mail(subject, message, 'jamalghazniwal@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post_share.html', {'form':form, 'sent':sent, 'post':post})
        
 

def home(request):
    post_list = Post.objects.all()
    return render(request, 'blog/home.html')


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)
    return render(request, 'blog/post_list.html', {'post_list':post_list, 'page': page})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)
    comments = post.comments.filter(is_active=True)
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags','-publish')[:4]
    
    form = CommentForm() 
    
    return render(request, 'blog/post_detail.html', 
                  {'post':post, 'comments':comments, 'form':form,
                   'similar_posts':similar_posts})

