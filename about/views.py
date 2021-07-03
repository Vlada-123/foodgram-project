from django.views.generic import TemplateView

app_name = 'about'


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutTechnologiesView(TemplateView):
    template_name = 'about/tech.html'
