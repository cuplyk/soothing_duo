from django.views.generic import TemplateView
from django.conf import settings


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class ContactsPageView(TemplateView):
    template_name = "pages/contacts.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["support_email"] = settings.SUPPORT_EMAIL
        context["support_number"] = settings.SUPPORT_NUMBER
        return context

class Blog(TemplateView):
    template_name = "pages/blog.html"    

class TicketPageView(TemplateView):
    template_name = "tickets/ticket.html" 

class TicketDashboardView(TemplateView):
    template_name = "tickets/dashboard.html" 