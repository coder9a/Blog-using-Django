from django.shortcuts import render
from django.http import HttpResponse
from home.models import Contact
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    messages.success(request, 'Welcome to About')
    return render(request, 'home/about.html')

def contact(request):
    messages.success(request, 'Welcome to Contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # print(name, email, phone, content)
        if len(name)<2 or len(email)<2 or len(phone)<10 or len(content)<2:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your form has been sent successfully!')
    return render(request, 'home/contact.html')
