from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
        if len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(content) < 2:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your form has been sent successfully!')
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allPosts = Post.objects.none()

    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if len(query) == 0:
        allPosts = Post.objects.none()
        messages.warning(
            request, 'No search results found. PLease refine your query')
    context = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', context)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 10:
            messages.error(
                request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('home')

        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, 'Your coder9a account has been successfully created')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')

    return HttpResponse('handleLogin')

def handleLogout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('home')