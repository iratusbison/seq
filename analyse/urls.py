from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_fastq, name='analyze_fastq'),
    #path('edit',views.edit_sequences, name= 'edit')
]
