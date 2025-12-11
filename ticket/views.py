from django.shortcuts import render

# Create your views here.
def ticket_view(request):
    return render(request, 'pages/ticket.html')