from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import websearching
from . import tasks

# Create your views here.

def func(request):
    if request.method == "POST":
        input_string = request.POST.get('name')
        tasks.cosinesimilarity(input_string)
        # return redirect('websearching')

    return render(request , 'websearching/index.html')    

    