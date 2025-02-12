from django.shortcuts import render, redirect
import openpyxl
from .forms import RecordForm
from django.db import models
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Create your views here.
from django.http import HttpResponse, request
from app.models import ExportadorXLSX
from .models import Record, SubGroup, Group
from django.urls import reverse_lazy

class BaseCargarArchivoView(View):
    template_name = 'app/cargar_archivo.html'
    model = None  # Debes especificar el modelo en las subclases
    delete_existing_records = True  # Agrega una variable para controlar la eliminación de registros existentes

    def cargar_datos(self, sheet):
        # Implementa la lógica de procesamiento de datos específica para cada tabla en las subclases
        raise NotImplementedError

    def post(self, request):
        archivo = request.FILES['archivo_excel']
        # Procesar el archivo Excel
        workbook = openpyxl.load_workbook(archivo)
        sheet = workbook.active

        if self.delete_existing_records:
            # Eliminar los registros existentes en la tabla
            self.model.objects.all().delete()

        # Cargar los datos en la base de datos
        self.cargar_datos(sheet)

        return redirect('index')  # Redirigir a la página inicial


def exportar_registros_view(request):
    exportador = ExportadorXLSX()
    nombre_archivo = exportador.exportar_registros()

    # Leer el contenido del archivo XLSX
    with open(nombre_archivo, 'rb') as archivo:
        contenido = archivo.read()

    # Crear una respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="registros_arranques_siembras.xlsx"'
    response.write(contenido)

    return response

def ajax_load_sub_groups(request):
    group_id = request.GET.get('group_id')
    # Verificar si el group_id es un valor numérico válido
    try:
        group_id = int(group_id)
    except (ValueError, TypeError):
        # Si el group_id no es un valor numérico válido, retornar una respuesta vacía
        return HttpResponse()
    
    sub_groups = SubGroup.objects.filter(group_id = group_id).order_by('name')
    return render(request, 'app/load_sub_groups.html', {'sub_groups': sub_groups})

class RecordListView(ListView):
    model = Record
    template_name = 'app/record_list.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'records'  # Nombre del objeto de contexto en la plantilla
    
    def get_queryset(self):
        # Excluimos los registros que tengan is_deleted=True
        return Record.objects.filter(is_deleted=False)
    
class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'app/record_create.html'  # Nombre de la plantilla a utilizar
    success_url = '/records/'  # URL a la que redirigir después de crear un registro exitosamente
    
    def form_valid(self, form):
        form.instance.save(user=self.request.user)
        return super().form_valid(form)
    
class RecordDetailView(DetailView):
    model = Record
    template_name = 'app/record_detail.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'record'  # Nombre del objeto de contexto en la plantilla
    
class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'app/record_update.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'record'  # Nombre del objeto de contexto en la plantilla
    success_url = '/records/'  # URL a la que redirigir después de actualizar un registro exitosamente
    
class RecordDeleteView(DeleteView):
    model = Record
    template_name = 'app/record_delete.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'record'  # Nombre del objeto de contexto en la plantilla
    success_url = reverse_lazy('app:record-list')  # URL a la que redirigir después de eliminar un registro exitosamente
    
