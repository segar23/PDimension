from django.views.generic import TemplateView


class LandingHome(TemplateView):
    template_name = 'landing/landing.html'


class AboutUsView(TemplateView):
    template_name = 'landing/about.html'
