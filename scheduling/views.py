from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage
from decouple import config

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "pages/contacts.html"
    success_url = reverse_lazy('contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["support_email"] = config("SUPPORT_EMAIL")
        context["support_number"] = config("SUPPORT_NUMBER")
        return context

    def form_valid(self, form):
        # Save the contact message
        response = super().form_valid(form)
        contact_message = self.object

        # Send Email
        subject = f"Nuovo messaggio da {contact_message.first_name} {contact_message.last_name}"
        message_body = (
            f"Hai ricevuto un nuovo messaggio dal sito web.\n\n"
            f"Dettagli contatto:\n"
            f"Nome: {contact_message.first_name}\n"
            f"Cognome: {contact_message.last_name}\n"
            f"Email: {contact_message.email}\n\n"
            f"Messaggio:\n{contact_message.message}"
        )
        recipient = config("SUPPORT_EMAIL")
        sender = config("EMAIL_HOST_USER")
        try:
            send_mail(
                subject,
                message_body,
                sender,
                [recipient],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't stop the user flow
            print(f"Error sending email: {e}")

        # Update the success message (this happens after super().form_valid in the original code, but we want it here)
        # Note: In the original code, messages.success was called BEFORE super().form_valid.
        # However, messages work across redirects, so calling it here is fine.
        # But wait, super().form_valid() in CreateView returns a HttpResponseRedirect.
        # So we should add the message BEFORE returning the response, which we are doing.
        # But we previously removed the original messages.success call which was before super().
        # Actually, let's keep the message.
        messages.success(self.request, "Messaggio inviato con successo! Ti risponderemo presto.")
        
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Si è verificato un errore. Per favore controlla i campi.")
        return super().form_invalid(form)