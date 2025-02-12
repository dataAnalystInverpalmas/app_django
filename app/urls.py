from django.urls import path
#from django.shortcuts import redirect
from . import views


app_name = 'app'  # Debes tener esta línea para registrar el espacio de nombres

urlpatterns = [
    path('records/', views.RecordListView.as_view(), name='record-list'),
    path('records/create/', views.RecordCreateView.as_view(), name='record-create'),
    path('records/<int:pk>/', views.RecordDetailView.as_view(), name='record-detail'),
    path('records/<int:pk>/update/', views.RecordUpdateView.as_view(), name='record-update'),
    path('records/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='record-delete'),
    
    path('ajax/load-sub-groups/', views.ajax_load_sub_groups, name='ajax_load_sub_groups'),  # <-- this one here
]
