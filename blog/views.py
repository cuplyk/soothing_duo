from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Category, Comment, Like
from django.db.models import Count

from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .forms import CommentForm, PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(status='published')
    
    # allows you to add additional context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            post__status='published'
        ).annotate(num_posts=Count('post')).order_by('name')
        return context 

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        # Get the post object
        post = super().get_object()
        
        # Increment views
        post.views += 1
        post.save(update_fields=['views'])
        
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        
        # Check if user liked the post
        if self.request.user.is_authenticated:
            context['liked'] = self.object.user_has_liked(self.request.user)
        else:
            # Check session for guest likes
            liked_posts = self.request.session.get('liked_posts', [])
            context['liked'] = self.object.id in liked_posts
        
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        #Show Number of Posts in Categories
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        #Fetches all category objects from database
        context['categories'] = Category.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['liked'] = self.object.user_has_liked(self.request.user)
    if self.request.htmx:
        context['htmx'] = True
    return context

# Like view
@require_POST
def like_toggle(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        # Authenticated user - use database
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
    else:
        # Guest user - use session
        if 'liked_posts' not in request.session:
            request.session['liked_posts'] = []
        
        liked_posts = request.session['liked_posts']
        
        if post.id in liked_posts:
            # Unlike
            liked_posts.remove(post.id)
            liked = False
        else:
            # Like
            liked_posts.append(post.id)
            liked = True
        
        request.session['liked_posts'] = liked_posts
        request.session.modified = True
    
    return render(request, 'blog/partials/like_button.html', {
        'post': post,
        'liked': liked
    })

# Comment views
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        if request.user.is_authenticated:
            comment.author = request.user
        # For guests, author is None, name/email come from form
        comment.save()
        
        return render(request, 'blog/partials/comment_item.html', {
            'comment': comment,
            'post': post
        })
        
    return HttpResponse(status=400)

def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'blog/partials/comment_edit.html', {
        'comment': comment
    })

@require_POST
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden()
        
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return render(request, 'blog/partials/comment_item.html', {
            'comment': comment
        })
        
    return HttpResponse(status=400)

def comment_item(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'blog/partials/comment_item.html', {
        'comment': comment
    })

# Infinite scroll
def posts_list(request):
    page = request.GET.get('page', 1)
    posts = Post.objects.filter(status='published').order_by('-created_at')
    
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)
    
    if page_obj.has_next():
        next_url = f"?page={page_obj.next_page_number()}"
    else:
        next_url = None
        
    context = {
        'posts': page_obj.object_list,
        'next_url': next_url
    }
    
    if request.htmx:
        return render(request, 'blog/partials/posts_list.html', context)
        
    return render(request, 'blog/post_list.html', context)