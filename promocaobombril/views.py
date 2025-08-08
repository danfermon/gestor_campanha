from django.shortcuts import render

def participe(request):
    # lógica da view
    return render(request, 'participe.html')
