from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Carrera
from .views import FormCarrera
from django.shortcuts import redirect, get_object_or_404

class CarreraCreateViewPage(TemplateView):
    template_name = 'carrera_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(instance=carrera)
        return self.render_to_response({'form': form})
    
    
class CarreraEditarViewPage(TemplateView):
    model = Carrera
    form_class = FormCarrera
    template_name = 'carrera_form.html'
    
    def post(self, request, *args, **kwargs):
        carrera = self.model.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        carrera = self.model.objects.get(pk=kwargs['pk'])
        form = FormCarrera(instance=carrera)
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

