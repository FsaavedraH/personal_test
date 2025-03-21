from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.db import IntegrityError

from .models import Personal
from .forms import PersonalForm  # Asegúrate de que esté bien importado

class PersonaListado(ListView):
    model = Personal

class PersonaCrear(SuccessMessageMixin, CreateView): 
    model = Personal 
    form_class = PersonalForm  
    success_message = 'Persona Creada Correctamente!' 

    def get_success_url(self):        
        return reverse_lazy('leer') 

    def form_invalid(self, form):
        # Verificar si el error es por cédula duplicada
        if "cedula" in form.errors:
            form.add_error("cedula", "Ya existe una persona registrada con esta cédula.")
        return self.render_to_response(self.get_context_data(form=form))
    
class PersonaDetalle(DetailView): 
    model = Personal
    
class PersonaActualizar(SuccessMessageMixin, UpdateView): 
    model = Personal 
    form_class = PersonalForm  
    template_name = "actualizar.html"
    success_message = 'Persona Actualizada Correctamente!' 
    success_url = reverse_lazy("leer")  # Asegurar que reverse_lazy se usa aquí

    def form_invalid(self, form):
        print("Errores en el formulario:", form.errors)  # Agregar depuración
        return self.render_to_response(self.get_context_data(form=form))
    
class PersonaEliminar(SuccessMessageMixin, DeleteView): 
    model = Personal
    success_message = "Persona Eliminada Correctamente!"  
    success_url = reverse_lazy('leer')  # Asegurar que use reverse_lazy

    def delete(self, request, *args, **kwargs):
        persona = get_object_or_404(Personal, pk=kwargs.get('pk'))
        print(f"🔴 Eliminando: {persona.nombre} {persona.apellido} (ID: {persona.pk})")
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

@csrf_exempt
def actualizar_asistencia(request, pk):
    if request.method == "POST":
        persona = get_object_or_404(Personal, pk=pk)
        persona.asistencia = not persona.asistencia  # Alterna el estado
        persona.save()
        return JsonResponse({"success": True, "asistencia": persona.asistencia})
    return JsonResponse({"success": False}, status=400)

def generar_reporte_asistencia(request):
    asistentes = Personal.objects.filter(asistencia=True)
    ausentes = Personal.objects.filter(asistencia=False)

    contenido = "Reporte de Asistencia\n\n"
    contenido += f"Total de Asistentes: {asistentes.count()}\n"
    contenido += "Lista de Asistentes:\n"
    for persona in asistentes:
        contenido += f"- {persona.nombre} {persona.apellido} (Cédula: {persona.cedula})\n"

    contenido += f"\nTotal de Ausentes: {ausentes.count()}\n"
    contenido += "Lista de Ausentes:\n"
    for persona in ausentes:
        contenido += f"- {persona.nombre} {persona.apellido} (Cédula: {persona.cedula})\n"

    response = HttpResponse(contenido, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="reporte_asistencia.txt"'
    return response

def guardar_asistencia(request):
    if request.method == "POST":
        for persona in Personal.objects.all():
            asistencia_key = f"asistencia_{persona.pk}"
            persona.asistencia = asistencia_key in request.POST
            persona.save()

        messages.success(request, "Asistencia guardada correctamente.")
    
    return redirect("leer")
