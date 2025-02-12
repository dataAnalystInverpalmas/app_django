from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
import mysql.connector
import openpyxl
from django.conf import settings
import os
import tempfile
from django.utils import timezone

class ConexionDB:
    def __init__(self):
        # Obtener los datos de conexión de DATABASES en settings.py
        database_settings = settings.DATABASES['default']
        
        # Establecer la conexión a la base de datos
        self.conn = mysql.connector.connect(
            user=database_settings['USER'],
            password=database_settings['PASSWORD'],
            host=database_settings['HOST'],
            database=database_settings['NAME']
        )
    
    def get_cursor(self):
        return self.conn.cursor()

    def close_conexion(self):
        self.conn.close()


class ExportadorXLSX(ConexionDB):
    def exportar_registros(self):
        # Obtener un cursor desde la conexión
        cursor = self.get_cursor()

        # Ejecutar consulta para obtener todos los registros de la tabla
        cursor.execute("SELECT * FROM arranques_siembras")
        registros = cursor.fetchall()

        # Crear un nuevo libro de trabajo de Excel
        libro = openpyxl.Workbook()

        # Seleccionar la hoja activa
        hoja = libro.active

        # Escribir los registros en el libro de trabajo
        for registro in registros:
            hoja.append(registro)

        # Guardar el libro de trabajo en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            nombre_archivo = temp_file.name + ".xlsx"
            libro.save(temp_file.name)
            os.rename(temp_file.name, nombre_archivo)

        # Cerrar el cursor y la conexión
        cursor.close()
        self.close_conexion()

        return nombre_archivo

class Production(models.Model):
    finca = models.CharField(max_length=100)
    bloque = models.IntegerField()
    nvari = models.CharField(max_length=100)
    cosecha = models.CharField(max_length=100)
    flor = models.CharField(max_length=100)
    matas = models.IntegerField()
    tallos = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return self.finca  # Puedes ajustar esto para mostrar el campo que desees en la representación de cadena del objeto
    
    
class Farm(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name
    
class GroupFlowers(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=3)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name


class Flower(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(GroupFlowers, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name
    
class Date(models.Model):
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return str(self.date)
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name
    
class DataType(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
        
    def __str__(self):
        return self.name
        


class SubGroup(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subgroups')
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name
    
class Record(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # otros campos del modelo
    
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    sub_group = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    really = models.FloatField(null=True, default=0)
    theoric = models.FloatField(null=True, default=0)
    goal = models.FloatField(null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def save(self, user=None, *args, **kwargs):
        if not self.pk and user is not None:  # Si el registro no existe aún (es una creación) y se ha proporcionado el usuario
            self.user = user
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Record #{self.pk}"
    
