from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Picture, Comment

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
