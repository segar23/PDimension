from django.views import View


class LandingHome(View):
    template_name = 'landing/landing.html'


class AboutUsView(View):
    template_name = 'landing/about.html'
