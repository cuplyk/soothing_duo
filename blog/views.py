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
        """
        Return the queryset of published posts to be displayed.

        Returns:
            QuerySet: A queryset of Post objects with the status "published".
        """
        return Post.objects.filter(status='published')
    
    # allows you to add additional context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(post__status='published').annotate(num_posts=Count('post')).order_by('name')
        return context 

class PostDetailView(DetailView):
    """
    A view that displays the details of a single blog post.

    This view increments the post's view count and provides context data for
    the post's comments and whether the current user has liked the post.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        """
        Return the post object.
        Returns:
            Post: The Post object that is being displayed.
        """
        # Get the post object
        post = super().get_object()
        
        return post
    
    def get_context_data(self, **kwargs):
        """
        Add additional context data to the template.

        This method adds the post's active comments and indicates whether the
        current user (authenticated or guest) has liked the post.

        Returns:
            dict: The context data for the template.
        """
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
    """
    A view that displays a list of published blog posts for a specific category.

    This view paginates the posts and provides additional context data, such as
    the category being viewed and a list of all categories.
    """
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """
        Return the queryset of published posts for the specified category.

        Returns:
            QuerySet: A queryset of Post objects filtered by category and
                status.
        """
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(category=self.category, status="published")
    
    def get_context_data(self, **kwargs):
        """
        Add additional context data to the template.

        This method adds the current category and a list of all categories to
        the context.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        #Show Number of Posts in Categories
        context['categories'] = Category.objects.annotate(num_posts=Count('post'))
        #Fetches all category objects from database
        context['categories'] = Category.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    A view that requires the user to be logged in and sets the author of the post
    to the current user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        """
        Set the author of the post to the current user.

        This method is called when the form is valid. It sets the author of the
        post to the currently logged-in user before saving the form.

        Args:
            form (PostForm): The valid form instance.

        Returns:
            HttpResponse: The response to redirect to the success URL.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view for updating an existing blog post.

    This view requires the user to be logged in and to be the author of the
    post. It sets the author of the post to the current user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        """
        Set the author of the post to the current user.

        This method is called when the form is valid. It sets the author of the
        post to the currently logged-in user before saving the form.

        Args:
            form (PostForm): The valid form instance.

        Returns:
            HttpResponse: The response to redirect to the success URL.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.

        This method is used by the UserPassesTestMixin to ensure that only the
        author of the post can edit it.

        Returns:
            bool: True if the current user is the author of the post, False
                otherwise.
        """
        post = self.get_object()
        return self.request.user == post.author


def get_context_data(self, **kwargs):
    
    """
    Add additional context data to the template.

    This function adds whether the current user has liked the post and whether
    the request is an HTMX request to the context.

    Returns:
        dict: The context data for the template.
    """
    context = super().get_context_data(**kwargs)
    context['liked'] = self.object.user_has_liked(self.request.user)
    if self.request.htmx:
        context['htmx'] = True
    return context

# Like view
@require_POST
def like_toggle(request, slug):
    """
    Toggle the like status of a post.

    This function handles the like toggle action for a post. It checks if the
    user is authenticated and uses the database to store likes. If the user is
    not authenticated, it uses the session to store likes.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the post to like.

    Returns:
        HttpResponse: The response to redirect to the post detail page.
    """
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
    """
    Add a comment to a post.

    This function handles the comment submission action for a post. It checks if the
    user is authenticated and uses the database to store comments. If the user is
    not authenticated, it uses the session to store comments.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the post to comment on.

    Returns:
        HttpResponse: The response to redirect to the post detail page.
    """
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
    """
    Edit a comment.

    This function handles the comment edit action for a post. It checks if the
    user is authenticated and uses the database to edit comments. If the user is
    not authenticated, it uses the session to edit comments.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the comment to edit.

    Returns:
        HttpResponse: The response to redirect to the post detail page.
    """
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'blog/partials/comment_edit.html', {
        'comment': comment
    })

@require_POST
def comment_update(request, pk):
    """
    Update a comment.

    This function handles the comment update action for a post. It checks if the
    user is authenticated and uses the database to update comments. If the user is
    not authenticated, it uses the session to update comments.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the comment to update.

    Returns:
        HttpResponse: The response to redirect to the post detail page.
    """
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
    """
    Display a list of posts.

    This function handles the display of a list of posts. It checks if the
    user is authenticated and uses the database to display posts. If the user is
    not authenticated, it uses the session to display posts.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response to render the posts list page.
    """
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