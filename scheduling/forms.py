from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Cognome',
            'email': 'Email',
            'message': 'Messaggio',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#080c0e] border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-[#D93A00] focus:ring-1 focus:ring-[#D93A00] transition-all',
                'placeholder': 'Mario'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#080c0e] border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-[#D93A00] focus:ring-1 focus:ring-[#D93A00] transition-all',
                'placeholder': 'Rossi'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-[#080c0e] border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-[#D93A00] focus:ring-1 focus:ring-[#D93A00] transition-all',
                'placeholder': 'mario.rossi@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-[#080c0e] border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-[#D93A00] focus:ring-1 focus:ring-[#D93A00] transition-all',
                'placeholder': 'Come possiamo aiutarti?',
                'rows': 3
            }),
        }
