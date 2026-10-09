import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Measurement
from .forms import MeasurementForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm

@login_required
def index(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect('index')
        else:
            print(form.errors) 
    
    measurements = Measurement.objects.filter(user=request.user).order_by('date')
    latest = measurements.last()
    
    week_ago = timezone.now() - timedelta(days=7)
    chart_data = measurements.filter(date__gte=week_ago)

    context = {
        'latest': latest,
        'measurements': measurements.order_by('-date'),
        'chart_labels': [m.date.strftime("%a") for m in chart_data],
        'upper_pressure_data': [m.upper_pressure for m in chart_data],
        'lower_pressure_data': [m.lower_pressure for m in chart_data],
        'form': MeasurementForm()
    }
    return render(request, 'index.html', context)

@login_required
def add_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect('index') 
    return redirect('index')

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response.write(u'\ufeff'.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename="health_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Дата', 'Верхнее', 'Нижнее', 'Пульс', 'Заметка'])    
    measurements = Measurement.objects.filter(user=request.user).order_by('-date')
    for m in measurements:
        writer.writerow([
            m.date.strftime("%d.%m.%Y %H:%M"), 
            m.upper_pressure, 
            m.lower_pressure, 
            m.pulse, 
            m.note
        ])
    
    return response

def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})