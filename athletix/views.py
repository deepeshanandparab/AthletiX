from django.shortcuts import render

def homePage(request):
    context = {'title': 'Home'}
    return render(request, 'athletix/home.html', context)