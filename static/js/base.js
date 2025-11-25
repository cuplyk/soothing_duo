// static/js/base.js
document.addEventListener('DOMContentLoaded', function() {
    // Like functionality with HTMX
    const likeForms = document.querySelectorAll('.like-form');
    likeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            htmx.ajax('POST', this.action, {
                values: {
                    csrfmiddlewaretoken: this.querySelector('[name=csrfmiddlewaretoken]').value
                },
                target: '#like-section',
                swap: 'innerHTML'
            });
        });
    });

    // Comment edit functionality
    const editButtons = document.querySelectorAll('.edit-comment-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            htmx.ajax('GET', `/comments/${commentId}/edit/`, {
                target: `#comment-${commentId}`,
                swap: 'innerHTML'
            });
        });
    });

    // Auto-expand textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states
    document.body.addEventListener('htmx:beforeRequest', function() {
        document.body.style.cursor = 'wait';
    });

    document.body.addEventListener('htmx:afterRequest', function() {
        document.body.style.cursor = 'default';
    });
});

// Custom filter for read time estimation
function readTimeFilter(text) {
    const wordsPerMinute = 200;
    const words = text.split(/\s+/).length;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min read`;
}