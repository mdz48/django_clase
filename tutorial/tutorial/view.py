from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Carrera
from .views import FormCarrera
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CarreraDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        carrera.delete()
        return redirect('home')
    

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
    
class CarreraEditarViewPage(TemplateView):
    template_name = 'carrera_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(instance=carrera)
        return self.render_to_response({'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})

class HomePageView(TemplateView):
    model = Carrera
    template_name = 'home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saludo"] = "Hola Mundo"
        context["lista"] = self.model.objects.all()    
        return context

class AboutPageView(TemplateView):
    template_name = 'about.html'

def index(request):
    return HttpResponse("Hello, world. You're at the tutorial index. CTM")

