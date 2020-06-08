from django.shortcuts import render

def aboutPage(request):
    context = {'title':'About'}
    return render(request, 'about/about.html', context)
