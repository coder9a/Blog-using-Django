from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def blogHome(request):
    return HttpResponse("Home blog")

def blogPost(request, slug):
    return HttpResponse(f'this is blogpost: {slug}')