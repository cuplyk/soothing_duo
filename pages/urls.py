from django.urls import path, include

from .views import HomePageView, AboutPageView, TicketPageView, TicketDashboardView
from scheduling.views import ContactView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("ticket/", TicketPageView.as_view(), name="ticket"),
    path("dashboard/", TicketDashboardView.as_view(), name="ticket_dashboard"),
    path("blog/", include('blog.urls')),
    
]
