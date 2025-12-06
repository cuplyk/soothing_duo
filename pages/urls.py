from django.urls import path, include

from .views import HomePageView, AboutPageView,ContactsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path("blog/", include('blog.urls')),
    
]
