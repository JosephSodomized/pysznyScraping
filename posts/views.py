from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # x = 1212;
    # return HttpResponse(x)
    return render(request, 'posts/index.html')