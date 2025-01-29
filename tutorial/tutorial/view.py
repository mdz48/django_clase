from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Carrera
from .views import FormCarrera
from django.shortcuts import redirect

class CarreraCreateViewPage(TemplateView):
    model = Carrera
    form_class = FormCarrera
    template_name = 'carrera_form.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormCarrera()
        context = { 'form': form }
        return self.render_to_response(context)

class HomePageView(TemplateView):
    model = Carrera
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saludo"] = "Hola Mundo"
        context["lista"]=self.model.objects.all()
        
        return context

    
    
class AboutPageView(TemplateView):
    template_name = 'about.html'

def index(request):
    return HttpResponse("Hello, world. You're at the tutorial index. CTM")

