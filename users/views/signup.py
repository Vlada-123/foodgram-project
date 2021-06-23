from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class SignUp(CreateView):
    """Регистрация."""
    form_class = CreationForm
    template_name = 'reg.html'
    success_url = reverse_lazy('login')
