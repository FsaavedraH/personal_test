from django.contrib import admin
from django.urls import path 
from  PersonalApp.views import PersonaListado, PersonaDetalle, PersonaCrear, PersonaActualizar, PersonaEliminar, generar_reporte_asistencia, actualizar_asistencia, guardar_asistencia


urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('', PersonaListado.as_view(template_name = "index.html"), name='leer'),
    
    path('personal/detalle/<int:pk>', PersonaDetalle.as_view(template_name = "detalles.html"), name='detalles'),
    
    path('personal/crear', PersonaCrear.as_view(template_name = "crear.html"), name='crear'),
    
    path('personal/editar/<int:pk>', PersonaActualizar.as_view(template_name = "actualizar.html"), name='actualizar'), 
    
    path('personal/eliminar/<int:pk>', PersonaEliminar.as_view(), name='eliminar'),
      
    path('reporte_asistencia/', generar_reporte_asistencia, name='reporte_asistencia'),
    
    path('actualizar_asistencia/<int:pk>/', actualizar_asistencia, name='actualizar_asistencia'),
    
    path('guardar_asistencia/', guardar_asistencia, name='guardar_asistencia'),
     
]