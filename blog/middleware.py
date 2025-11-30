class PostViewCounterMiddleware:
    """
    Middleware to track and increment view counts for blog posts.
    
    This middleware automatically increments the view counter
    when a user accesses a blog post detail page.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware/handler in the chain
        """
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Process each request and increment post views if applicable.
        
        Args:
            request: The HTTP request object
            
        Returns:
            response: The HTTP response object
        """
        # Process the request through the rest of the middleware chain
        # and get the response
        response = self.get_response(request)
        
        # Check if this request is for a blog post detail page
        # - Verify that resolver_match exists (not None for valid URLs)
        # - Check if the view name matches 'blog:post_detail'
        if (request.resolver_match and 
            request.resolver_match.view_name == 'blog:post_detail'):
            
            # Extract the post object from URL kwargs
            # This assumes the URL pattern includes a 'post' parameter
            post = request.resolver_match.kwargs.get('post')
            
            # If a post object was found in the URL, increment its view count
            if post:
                post.views += 1  # Increment the view counter
                post.save(update_fields=['views'])  # Save only the views field for efficiency
                
        return response