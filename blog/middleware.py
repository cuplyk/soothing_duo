class PostViewCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        if 'blog:post_detail' in request.resolver_match.view_name:
            post = request.resolver_match.kwargs.get('post')
            if post:
                post.views += 1
                post.save(update_fields=['views'])
                
        return response