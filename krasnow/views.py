from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return HttpResponse("Welcome to the Krasnow CSV2DB capability.")
    return render(request, 'krasnow/index.html')
