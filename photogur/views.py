from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Picture, Comment
from photogur.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

def root(request):
    return HttpResponseRedirect('pictures')

def picture_page(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query) | Picture.objects.filter(title=query)
    context = {'pictures': search_results, 'query': query}
    response = render(request, 'search.html', context)
    return HttpResponse(response)

def create_comment(request):
    picture = request.POST['picture']
    comment = request.POST['new-comment']
    new_comment = Comment.objects.create(name=request.POST['name'],
                                         message=request.POST['new-comment'],
                                         picture=Picture.objects.get(pk=request.POST['picture'])
                                         )
    return HttpResponseRedirect('/pictures/'+ request.POST['picture'])

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures/')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    # form = LoginForm()
    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures/')
